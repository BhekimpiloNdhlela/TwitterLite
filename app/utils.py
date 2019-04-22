#!usr/bin/python
"""
"""
import os
import re
from passlib.hash import sha512_crypt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from itsdangerous import URLSafeTimedSerializer

def validatePassword(formInput, debug=True):
    """ uses regular expression to validate password strength """
    return True

def validateDate(formInput, debug=True):
    """ uses regular expression to validate password strength """
    return True
5
def validateName(formInput, debug=True):
    """ uses regular expression to validate password strength """
    return True

def validateSurname(formInput, debug=True):
    """ sumary_line """
    return True

def processPicture(formInput, debug=True):
    """ sumary_line """
    return True

def comparePassword(this, that, debug=True):
    """ sumary_line """
    return True


def updatePassword(newpassword, oldpassword, debug=True):
    """ sumary_line """
    return True

def passwordHash(password, debug=True):
    """ sumary_line """
    return True

def getDate():
    """ sumary_line """
    return None

def detTimeStamp():
    """ sumary_line """
    return None

def sendRessetPasswordEmail(to_email, from_email='resetpassword@bootlegtwitter.com'):
    """ sumary_line """
    return None

def sendForgotPasswordEmail(to_email, token, from_email='forgotpassword@bootlegtwitter.com'):
    """ sumary_line """
    pass

def sendAccountVerificationEmail(to_email, token, from_email='verifyaccount@bootlegtwitter.com'):
    """ sumary_line """
    return None

def sendEmailTest(to_email='0000000@sun.ac.za', from_email='verifyaccount@bootlegtwitter.com'):
    """ sumary_line """
    #TODO: change the to_email it the signature to you email adress to test if your configuration is successful
    #TODO: set this in config.cnf file
    salt = URLSafeTimedSerializer("ThisIsASecretSaltString")
    message = Mail(     from_email=from_email,
                        to_emails=to_email,
                        subject='Verify Account',
                        html_content='<strong>and easy to do anywhere, even with Python</strong>'
    )

    try:
        # TODO: check the readme to configure the send grid API_KEY in the README.md file
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        if response.status_code == 202:
            pass #success
        else:
            pass #error
    except Exception as e:
        print(e.message)

DEBUG = False
if DEBUG:
    sendEmailTest()