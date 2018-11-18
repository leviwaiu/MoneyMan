from flask import render_template, flash, redirect, request, url_for
from app import app, db
from flask_login import current_user, login_user, login_required, logout_user
from app.models import *
from app.forms import LoginForm, RegistrationForm, CategoriesForm, TransactionForm
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    current_user.check_bank_valid()
    return render_template('index.html', title='Home')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username). first_or_404()
    return render_template('user.html', user=user)

@app.route('/control', methods=['GET', 'POST'])
@login_required
def control():
    form=CategoriesForm();
    if form.is_submitted():
        controlamount = 0;
        print(form.control.data)
        if form.control.data:
            controlamount = form.ctrl_amount.data
        else:
            controlamount = None
            
        categories = Category(name=form.name.data, constraint = controlamount, remaining=controlamount, owner=current_user)
        db.session.add(categories)
        db.session.commit()
        return redirect(url_for('control'))
    return render_template('control.html', user=user, form=form)
    
@app.route('/monitor', methods=['GET', 'POST'])
@login_required
def monitor():
    form = TransactionForm()
    form.setChoices()
    current_user.update_Balance()
    if form.validate_on_submit():
        print(form.item_id.data)
        cat = form.transactionCat.data
        item_id = int(form.item_id.data)
        Transaction.query.get(item_id).category = Category.query.filter_by(name=cat).first()
        print(Category.query.filter_by(name=cat).first())
        Category.query.filter_by(name=cat).first().subRemaining(Transaction.query.get(item_id).amount)
        db.session.commit()
        return redirect('/monitor')
    return render_template('monitor.html', form=form)
