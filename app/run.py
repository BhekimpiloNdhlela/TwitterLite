#!usr/bin/python

"""
"""
from utils import *
from flask import Flask, request, session, redirect, url_for, render_template, flash

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


@app.route('/signin')
def login():
    """
    """
    return render_template('login.html')

@app.route('/signup')
def register():
    """
    """
    return render_template('register.html')

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
    return help(passlib.hash)

@app.route('/logout')
def logout():
    """
    """
    return '<h1>Loging Out</h1>'

if __name__ == '__main__':
    app.run(debug=True)
else:
    from sys import exit
    exit('usage: python2 run.py')