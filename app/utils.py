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
    #TODO: set this in config.cnf file
    verrification_link = 'http://localhost:5000/confirm-email/'+token
    salt = URLSafeTimedSerializer("ThisIsASecretSaltString")
    html_content = '<h2>The Following is your account verification link From BootlegTwitter:<h2><br>'
    html_content += '<strong>Please follow the following link to verify your account</strong><br>'

    html_content += '<a href=\"{}\">Click to verify your email address</a>'.format(verrification_link)

    msg = Mail(from_email=from_email, to_emails=to_email, subject='Verify Account', html_content=html_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(msg)
        if response.status_code == 202:
            pass #success
        else:
            pass #error
    except Exception as e:
        print(e.message)