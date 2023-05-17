from flask import Blueprint, Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db, User, Vendor
from form import SignupForm, LoginForm, VendorForm

app = Flask(__name__)

# Initialize the LoginManager
login_manager = LoginManager(app)
login_manager.init_app(app)

login_manager.login_view = 'auth.login'

# Register the blueprint for the auth module
auth_app = Blueprint('auth', __name__)

# This function should load the user by their ID, which is passed as an argument to the function.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        new_user = User(name=form.name.data, email=form.email.data, phone_number=form.phone_number.data, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth_app.route('/vendor-signup', methods=['GET', 'POST'])
def vendor_signup():
    form = VendorForm()
    if form.validate_on_submit():
        vendor = Vendor.query.filter_by(email=form.email.data).first()
        if vendor:
            flash('Email address already exists')
            return redirect(url_for('auth.vendor-signup'))
        new_vendor = Vendor(name=form.name.data, email=form.email.data, phone_number=form.phone_number.data, address=form.address.data, company_name=form.company_name.data, description=form.description.data, password=generate_password_hash(form.password.data))
        new_user = User(name=form.name.data, email=form.email.data, phone_number=form.phone_number.data, password=generate_password_hash(form.password.data))
        db.session.add(new_vendor, new_user)
        db.session.commit()
        login_user(new_vendor)
        return redirect(url_for('auth.login'))
    return render_template('vendor_signup.html', form=form)

@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_type = form.user_type.data

        # Check the user type and fetch the corresponding user from the database
        if user_type == 'user':
            user = User.query.filter_by(email=email).first()
        elif user_type == 'vendor':
            user = Vendor.query.filter_by(email=email).first()
        else:
            user = None

        if user and check_password_hash(user.password, password):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully.')
            return redirect(url_for('items.allItems'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@auth_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('items.allItems'))