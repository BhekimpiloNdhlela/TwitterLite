#!usr/bin/python3
#TODO: All the sectret keys, salts should be placed in a config

from utils import *
from flask import Flask, request, session, redirect, url_for, render_template, flash
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader, Template

#TODO: remains in the run.py when moving goes down
app = Flask(__name__)


#TODO: this has to be changed. the salt should be set in a config file
salt = URLSafeTimedSerializer("ThisIsASecretSaltStringURLSafeTimedSerializerURLSafeTimedSerializer")

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

@app.route('/')
@app.route('/home')
def home():
    """ sumary_line """
    return render_template('index.html')

@app.route('/about')
def about():
    """ sumary_line """
    return render_template('about.html')

@app.route('/password')
def forgot_password():
    """ sumary_line """
    return render_template('forgot-password.html')

@app.route('/login')
@app.route('/signin')
def login():
    """ sumary_line """
    return render_template('login.html')

@app.route('/editprofile')
def editUserProfile():
    """ sumary_line """
    pass

@app.route('/changepassword')
def changeUserPassword():
    """ sumary_line """
    pass

@app.route('/viewprofile')
def viewUserBio():
    """ sumary_line """
    template = env.get_template("index.html")
    return template.render(name="John")

@app.route('/logout')
def logout():
    """ sumary_line """
    return '<h1>Loging Out</h1>'

@app.route('/signup', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    """ sumary_line """
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form['email']
        token = salt.dumps(email, salt='email-confirm')
        # TODO:  make use of the send account verification email using the utils function.
        sendAccountVerificationEmail(email, token)
        # TODO: the following line should be a bootstrap alert notifying the user that an email has been sent
        return '<h1>Please verify email: {}. with the following token: {}</h1>'.format(email, token)


@app.route('/verify-email/<token>')
@app.route('/confirm-email/<token>')
def confirmEmail(token):
    """ sumary_line """
    #TODO: this logic should go to the backend
    try:
        email = salt.loads(token, salt='email-confirm', max_age=30)
    except SignatureExpired:
        return '<h1> the token has expired</h1>'
    return '<h1>Email: {} has been verified</h1>'.format(email)

if __name__ == '__main__':
    app.run(debug=True)
else:
    from sys import exit
    exit('usage: python2 run.py')