#!usr/bin/python
"""
TODO: All the sectret keys, salts should be placed in a config
"""

from utils import *
from flask import Flask, request, session, redirect, url_for, render_template, flash
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    """
    """
    return render_template('index.html')

@app.route('/about')
def about():
    """
    """
    return render_template('about.html')

@app.route('/password')
def forgot_password():
    """
    """
    return render_template('forgot-password.html')


@app.route('/login')
@app.route('/signin')
def login():
    """
    """
    return render_template('login.html')


@app.route('/editprofile')
def editUserProfile():
    """
    """
    pass

@app.route('/changepassword')
def changeUserPassword():
    """
    """
    pass

@app.route('/viewprofile')
def viewUserBio():
    """
    """
    return '<h1>View Profile</h1>'

@app.route('/logout')
def logout():
    """
    """
    return '<h1>Loging Out</h1>'

"""
TODO: this has to be changed. the salt should be set in a config file
"""
salt = URLSafeTimedSerializer("ThisIsASecretSaltStringURLSafeTimedSerializerURLSafeTimedSerializer")

@app.route('/signup', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    """
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form['email']
        token = salt.dumps(email, salt='email-confirm')
        #TODO:  make use of the send account verification email using the utils function.
        sendAccountVerificationEmail(email, token)
        #TODO: the following line should be a bootstrap alert notifying the user that an email has been sent
        sendAccountVerificationEmail(email, token)
        return '<h2>The verification Email Has been sent please check you email inbox<h2>'

@app.route('/verify-email/<token>')
@app.route('/confirm-email/<token>')
def confirmEmail(token):

    #TODO: this logic should go to the backend
    try:
        email = salt.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1> the token has expired</h1>'
    return '<h1>Email: {} has been verified</h1>'.format(email)

if __name__ == '__main__':
    app.run(debug=True)
else:
    from sys import exit
    exit('usage: python2 run.py')