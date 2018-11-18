from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from hashlib import md5
from app.api import getAccount, getCustomerList
import datetime

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    account_id = db.Column(db.String(128))
    accounts = db.relationship('Account', backref='owner', lazy='dynamic')
    categories = db.relationship('Category', backref='owner', lazy='dynamic')
    transactions = db.relationship('Transaction', backref="owner", lazy='dynamic')
    
    streetNo = db.Column(db.String(128))
    street = db.Column(db.String(128))
    city = db.Column(db.String(128))
    state = db.Column(db.String(128))
    zipcode = db.Column(db.String(128))
    
    def getCategories(self):
        return self.categories
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def check_bank_valid(self):
        customerList = getCustomerList()
        for entry in customerList:
            if self.first_name == entry['first_name'] and self.last_name == entry['last_name']:
                self.account_id = entry['_id']
                
                add = entry['address']
                self.streetNo = add['street_number']
                self.street = add['street_name']
                self.city = add['city']
                self.state = add['state']
                self.zipcode = add['zip']
                self.check_Accounts()
                
    def check_Accounts(self):
        accountList = getAccount(self.account_id, "")
        for account in accountList:
            prevAccounts = Account.query.filter_by(code=account['_id']).first()
            if prevAccounts is None:
                account = Account(code= account['_id'], balance = account['balance'], nickname = account['nickname'], accType = account['type'], owner=current_user)
                db.session.add(account)
                db.session.commit()
    
    def update_Balance(self):
        for acc in self.accounts:
            difference = acc.checkBalance()
            if difference != 0:
                acc.updateBalance()
                trans = Transaction(amount=difference,owner=current_user, time= datetime.datetime.now())
                db.session.add(trans)
                db.session.commit()
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code= db.Column(db.String(128), index=True, unique=True)
    balance=db.Column(db.Integer)
    nickname=db.Column(db.String(128))
    accType = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    def checkBalance(self):
        apiAccount = getAccount("", self.code)
        newBalance = apiAccount['balance']
        print(self.code)
        return self.balance - newBalance
    
    def updateBalance(self):
        apiAccount = getAccount("",self.code)
        self.balance = apiAccount['balance']
    
    def __repr__(self):
        return '<Account {}>'.format(self.code)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    constraint = db.Column(db.Float)
    remaining = db.Column(db.Float)
    belonging_transactions = db.relationship('Transaction', backref="category", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def subRemaining(self, deduction):
        if self.remaining is not None:
            self.remaining -= deduction
            if self.remaining < 0:
                self.name += "[OVERBUDGET]"
            
    def __repr__(self):
        return '<Category {} {}>'.format(self.id, self.name)
    
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    amount = db.Column(db.Float)
    time = db.Column(db.DateTime)
    recipient = db.Column(db.String(128))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Transaction {}>'.format(self.id)
