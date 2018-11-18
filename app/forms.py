from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, SelectField, HiddenField
from app.models import User, Category 
from app.api import getAccount, getCustomerList
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_names(self, first_name, last_name):
        first = User.query.filter_by(first_name=first_name.data).first()
        last = User.query.filter_by(last_name=last_name.data).first()
        if first is not None and last is not None:
            raise ValidationError("You have already signed in with us.")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')
class CategoriesForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    control = BooleanField('Control Spending')
    ctrl_amount = DecimalField('Spend Under:')
    submit = SubmitField('Add Category')
    
class TransactionForm(FlaskForm):
    item_id = HiddenField()
    transactionCat = SelectField()
    submit = SubmitField("Confirm Changes")
    
    def setChoices(self):
        options = []
        from flask_login import current_user
        categories = current_user.categories
        for cat in categories:
            options.append((cat.name, cat.name))
        self.transactionCat.choices = options
            
    
    
