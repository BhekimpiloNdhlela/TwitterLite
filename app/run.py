#!usr/bin/python
from flask import Flask
from utils import *
from flask import Flask, request, session, redirect, url_for, render_template, flash

import passlib

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    pass

@app.route('/register')
def register():
    pass

@app.route('/editprofile')
def editUserProfile():
    pass

@app.route('/changepassword')
def changeUserPassword():
    pass

@app.route('/viewprofile')
def viewUserBio():
    return help(passlib.hash)

if __name__ == '__main__':
    app.run(debug=True)
else:
    from sys import exit
    exit('usage: python2 run.py')