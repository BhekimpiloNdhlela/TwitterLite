#!usr/bin/python
"""
"""
import os
import re
from passlib.hash import sha512_crypt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from itsdangerous import URLSafeTimedSerializer
from datetime import date, datetime


def get_date():
    """
    used to get todays date, this is done when a user is creating a post or when the user is creating
    an account. Essentially this function is used for anything that needs today's date.
    """
    todays_date = date.today().strftime("%Y-%m-%d")
    return todays_date


def get_time_stamp():
    """
    used to get the now's time stamp, this is done when a user is creating a post or when the user is
    creating an account. Essentially this function is used for anything that needs a now's timestamp.
    """
    time_stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    return time_stamp


def get_password_hash(password, salt='THESALTISsaltyLi', rounds=99999):
    """
    used to obtain a users password hash, since password should not be stored in the database explicitly
    this function makes use of the sha512_crypt algorithm to make hashes with the default rounds.
    """
    hash = sha512_crypt.encrypt(password, salt=salt, rounds=rounds)
    return hash


def send_resset_password_email(to_email, from_email='resetpassword@bootlegtwitter.com'):
    """
    """
    subject = 'Password Changed'
    html_content = '<h2>BootlegTwitter Password changed Notification<h2><br>'
    html_content += '<strong>The password for the following account has been changed</strong><br>'
    html_content += '<p>Account: {}</p>'.format(to_email)
    __send_email(from_email, to_email, subject, html_content)


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


def validate_password(formInput, debug=True):
    """ uses regular expression to validate password strength """
    return True


def validate_date(formInput, debug=True):
    """ uses regular expression to validate password strength """
    return True


def validate_name(formInput, debug=True):
    """ uses regular expression to validate password strength """
    return True


def validate_surname(formInput, debug=True):
    """ sumary_line """
    return True


def process_picture(form_input, debug=True):
    """ sumary_line """
    return True


def compare_password(this, that, debug=True):
    """ sumary_line """
    return True


def update_password(newpassword, oldpassword, debug=True):
    """ sumary_line """
    return True
