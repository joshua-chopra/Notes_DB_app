# imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

# set up blueprint
auth = Blueprint('auth', __name__)


# we want to accept both GET and POST (to render HTML, and to grab user's input and deal w/ the POST request from form)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist. Redirecting you to the sign up page...', category='error')
            # sleep for 2 seconds before redirecting
            # time.sleep(5.0)
            # call sign_up func in this blueprint and redirect user to sign up page
            return redirect((url_for('.sign_up')))

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect((url_for('.login')))


"""
Register endpoint w/ sign up page, set up to create a new user if they input valid information into our form, 
"""


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # when accessing in route, has all the data sent when this route was accessed,
    # that was sent as part of the form that sends a POST request.
    if request.method == 'POST':
        # redirect user upon signing up to the home page where they can enter their notes, log user in DB.
        if user_info := validate_sign_up_info(request):
            print(f'valid sign up credentials which are: {user_info}.')
            new_user = User(email=user_info['email'], first_name=user_info['first_name'],
                            password=generate_password_hash(user_info['password'], method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            logged_in = login_user(new_user, remember=True)
            if not logged_in:
                print('error, unable to log in user.')
            flash('Account created!', category='success')
            # return redirect to home function blueprint (views) which redirects to the homepage.
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


"""
Validate sign up information and flash corresponding error messages if needed, or success if account was created.
Return information from form (email, first name, password) or empty dict if nothing. 
"""


def validate_sign_up_info(message: request) -> dict:
    # get attributes from form
    email = request.form.get('email')
    # address case of user attempting to sign up again to avoid attempting duplicate insert into db.
    if User.query.filter_by(email=email).first():
        flash('You already have an account! Please login.', category='error')
        return {}
    first_name = request.form.get('firstName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    # we'll need user to re-enter info in these cases
    if len(email) < 4:
        flash('Email must be greater than 3 characters, please please re-enter.', category='error')
        return {}
    elif len(first_name) < 2:
        flash('First name must be at least 2 characters, please please re-enter.', category='error')
        return {}
    elif password1 != password2:
        flash('Passwords don\'t match, please re-enter..', category='error')
        return {}
    elif len(password1) < 7:
        flash('Password must be at least 7 characters, please re-enter.', category='error')
        return {}
    else:
        # flash('Account created! Please navigate to login page to access your notes.', category='success')
        return {'email': email, 'first_name': first_name, 'password': password1}
