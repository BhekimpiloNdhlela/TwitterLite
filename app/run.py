#!usr/bin/python3
# TODO: All the sectret keys, salts should be placed in a config

from utils import *
from flask import Flask, request, session, redirect, url_for, render_template, flash
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired
from jinja2 import Environment, select_autoescape, FileSystemLoader

from mock_data import *
from models import *

# TODO: remains in the run.py when moving goes down
app = Flask(__name__)


# TODO: this has to be changed. the salt should be set in a config file
salt = URLSafeTimedSerializer(
    "ThisIsASecretSaltStringURLSafeTimedSerializerURLSafeTimedSerializer")

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)


@app.route('/')
@app.route('/home')
def home():
    """ sumary_line """
    template = env.get_template("index.html")
    user = User("john_doe")
    return template.render(user=user, tweets=mock_tweets, treading=mock_treading, account=True)


@app.route('/friends')
def friends():
    """ sumary_line """
    template = env.get_template("friends.html")
    return template.render(user=john_doe, tweets=mock_tweets, treading=mock_treading)


@app.route('/about')
def about():
    """ sumary_line """
    template = env.get_template("about.html")
    return template.render()


@app.route('/password', methods=['GET', 'POST'])
def forgot_password():
    """ sumary_line """
    if request.method == 'POST':
        pass
    template = env.get_template("forgot-password.html")
    return template.render()


@app.route('/login', methods=['GET', 'POST'])
@app.route('/signin', methods=['GET', 'POST'])
def login():
    """ sumary_line """
    if request.method == 'POST':
        pass
    template = env.get_template("login.html")
    return template.render()


@app.route('/account')
def account():
    """ sumary_line """
    template = env.get_template("account.html")
    return template.render(user=john_doe, tweets=mock_tweets, treading=mock_treading)


@app.route('/messages')
def messages():
    """ sumary_line """
    template = env.get_template("messages.html")
    return template.render(user=john_doe, tweets=mock_tweets, treading=mock_treading)


@app.route('/changepassword')
def change_user_password():
    """ sumary_line """
    pass

# TODO Must implement - Get user data from db
@app.route('/profile/<username>')
def view_user_bio():
    """ sumary_line """
    template = env.get_template("index.html")
    return template.render(user=john_doe, tweets=mock_tweets, treading=mock_treading, account=False)


@app.route('/logout')
def logout():
    """ sumary_line """
    return '<h1>Loging Out</h1>'


@app.route('/signup', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    """ sumary_line """
    if request.method == 'POST':
        # user form input should be processed and verified
        email = request.form['email']
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dob = get_date_string(request.form['dob'])
        gender = request.form['gender']
        password0 = request.form['password']
        password1 = request.form['password1']
        user = User(username)
        user.add_user(firstname, lastname, email, dob, gender, get_password_hash(password0))
        token = salt.dumps(username, salt='email-confirm')
        send_account_verification_email(email, token)
        return '<h2>The verification Email Has been sent please check you email inbox<h2>'
    template = env.get_template("register.html")
    return template.render()


@app.route('/verify-email/<token>')
@app.route('/confirm-email/<token>')
def confirm_email(token):
    """ sumary_line """
    try:
        username = salt.loads(token, salt='email-confirm', max_age=3600)
        user = User(username)
        user.verify_user_account()
        email = user.get_user_email()
        return '<h1>Email: {} has been verified</h1>'.format(email)
    except SignatureExpired:
        return '<h1> the token has expired</h1>'


@app.route('/set-new-password', methods=['GET', 'POST'])
def set_new_password(token):
    pass


if __name__ == '__main__':
    app.run(debug=True)
else:
    from sys import exit
    exit('usage: python2 run.py')
