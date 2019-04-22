#!usr/bin/python
"""
"""
import os
import re
from passlib.hash import sha512_crypt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from itsdangerous import URLSafeTimedSerializer

def validate_password(formInput, debug=True):
    """ uses regular expression to validate password strength """
    return True

def validate_date(formInput, debug=True):
    """ uses regular expression to validate password strength """
    return True
5
def validate_name(formInput, debug=True):
    """ uses regular expression to validate password strength """
    return True

def validate_surname(formInput, debug=True):
    """ sumary_line """
    return True

def process_picture(formInput, debug=True):
    """ sumary_line """
    return True

def compare_password(this, that, debug=True):
    """ sumary_line """
    return True


def update_password(newpassword, oldpassword, debug=True):
    """ sumary_line """
    return True

def password_hash(password, debug=True):
    """ sumary_line """
    return True

def get_date():
    """ sumary_line """
    return None

def set_time_stamp():
    """ sumary_line """
    return None

def send_resset_password_email(to_email, from_email='resetpassword@bootlegtwitter.com'):
    """ sumary_line """
    return None

def send_forgot_password_email(to_email, token, from_email='forgotpassword@bootlegtwitter.com'):
    """
    used to send account verification email to the user. This function is call only when the user
    needs to reset his/her password after loosing it.
    """
    verrification_link = 'http://localhost:5000/set-new-password/'+token
    subject = 'Forgot Password'
    html_content = '<h2>The Following is your Password Reset link From BootlegTwitter:<h2><br>'
    html_content += '<strong>Please Click the following link to Change Your Password</strong><br>'
    html_content += '<a href=\"{}\">Click to Reset password</a>'.format(verrification_link)
    __send_email(from_email, to_email, subject, html_content)


def send_account_verification_email(to_email, token, from_email='verifyaccount@bootlegtwitter.com'):
    """
    used to send account verification email to the user. this function is used only once,
    this is when a user is creating an account at BootlegTwitter for the first time.
    """
    verrification_link = 'http://localhost:5000/confirm-email/'+token
    subject = 'Account Verification'
    html_content = '<h2>The Following is your account verification link From BootlegTwitter:<h2><br>'
    html_content += '<strong>Please Click the following link to verify your account</strong><br>'
    html_content += '<a href=\"{}\">Click to verify your email address</a>'.format(verrification_link)
    __send_message(from_email, to_email, subject, html_content)



def __send_email(from_email, to_email, subject, html_content):
    """
    [private/ helper] function to send emails, to the user at hand. This helper function can be used
    to send account verrification, password reset and forgot password emails.

    NOTE: this function is never called directly hence the {__send_email} notation.

    """
    msg = Mail(from_email=from_email, to_emails=to_email, subject=subject, html_content=html_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(msg)
    except Exception as e:
        print(e.message)