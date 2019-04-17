#!usr/bin/python
from flask import Flask, render_template
from utils import *

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return '<h1>Hello World!</h1>'

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
    pass

@app.route('/about')
def about():


if __name__ == '__main__':
    app.run(debug=True)

else:
    pass