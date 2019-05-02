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
# TODO: add this to the config file
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# TODO: this has to be changed. the salt should be set in a config file
salt = URLSafeTimedSerializer(
    'ThisIsASecretSaltStringURLSafeTimedSerializerURLSafeTimedSerializer'
)

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

@app.route('/')
@app.route('/home')
@app.route('/login', methods=['GET', 'POST'])
@app.route('/signin', methods=['GET', 'POST'])

def home():
    """ sumary_line """
    """
    template = env.get_template("index.html")
    user = User(session['username']).get_json_user()
    #user = john_doe
    return template.render(user=user, tweets=mock_tweets, treading=mock_treading, account=True)
    """
    """ sumary_line """
    if request.method == 'POST':
        #TODO: user regualr expression to validate user input
        username = request.form['username']
        password = request.form['password']
        user     = User(username)
        login_status = user.user_login(password)

        if login_status == -1:
            return ('Invalid user account please check your username.')
        elif login_status == -2:
            return ('Account not verified, please check you email to verify account.')
        elif login_status == True:
            session['username'] = username
            return render_template('index.html', user=user.get_json_user(), tweets=mock_tweets, treading=mock_treading, account=True)
        elif login_status == False:
            return ('Wrong password, please check your password or change it if you forgot the password.')

    template = env.get_template("login.html")
    return template.render()



@app.route('/friends')
def friends():
    """ sumary_line """
    template = env.get_template("friends.html")
    return template.render(user=john_doe, tweets=mock_tweets, treading=mock_treading, following=mock_following, followers=mock_followers, personaltweets=mock_personal)


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


@app.route('/account')
def account():
    """ sumary_line """
    template = env.get_template("account.html")
    user = User(session['username']).get_json_user()
    return template.render(user=user, tweets=mock_tweets, treading=mock_treading)


@app.route('/messages')
def messages():
    """ sumary_line """
    template = env.get_template("messages.html")
    return template.render(user=john_doe, tweets=mock_tweets, treading=mock_treading, messages=mock_messages)


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
    session.pop('username', None)
    flash('Logged out.')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    """ sumary_line """
    if request.method == 'POST':
        #TODO: user regualr expression to validate user input
        email     = request.form['email']
        username  = request.form['username']
        firstname = request.form['firstname']
        lastname  = request.form['lastname']
        dob       = request.form['dob']
        gender    = request.form['gender']
        password0 = request.form['password']
        password1 = request.form['password1']
        if password0 != password1:
            return ('passwords do not match')
        if not validate_date(password0):
            return ('Password should be at least 9 chars, A-Za-z0-9')
        user = User(username)
        if not user.get_this_user_data():
            user.add_user(firstname, lastname, email, dob, gender, get_password_hash(password0))
            token = salt.dumps(username, salt='email-confirm')
            send_account_verification_email(email, token)
            return ('a verification Email Has been sent please check you email inbox')
        else:
            return ('This username already exits please select a new user name')
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
        flash('This token has expired')


@app.route('/set-new-password', methods=['GET', 'POST'])
def set_new_password(token):
    if request.method == 'POST':
        # TODO: user regualr expression to validate user input
        if request.form['newpassword0'] == request.form['newpassword1']:
            oldpassword = request.form['oldpassword']
            user        = User(session['username'])
            if get_password_verification(user.get_password_hash(), oldpassword):
                user.update_password_hash(request.form['newpassword0'])
                send_resset_password_email(user.get_user_email())
                flash('Password updated.')
            else:
                flash('Wrong password, please try again.')
        else:
            flash('Password do not match, please try again.')


if __name__ == '__main__':
    app.run(debug=True)
else:
    from sys import exit
    exit('usage: python2 run.py')
