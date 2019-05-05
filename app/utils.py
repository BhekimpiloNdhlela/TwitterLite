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


def get_time_stamp():
    """
    used to get the now's time stamp, this is done when a user is creating a
    post or when the user is creating an account. Essentially this function is
    used for anything that needs a now's timestamp.
    """
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')


def get_formated_date(formatingdate):
    """
    used to get todays date, this is done when a user is creating a post or when
    the user is creating an account. Essentially this function is used for
    anything that needs today's date.
    """
    return datetime.strptime(formatingdate, '%Y-%m-%d')


def get_date_string():
    """
    used to get todays date, this is done when a user is creating a post or when
    the user is creating an account. Essentially this function is used for anything
    that needs today's date.
    """
    return  date.today().strftime('%d-%m-%Y')


def get_timestamp_seconds():
    """
    used to get the now's time stamp, this is done when a user is creating a post
    or when the user is creating an account. Essentially this function is used
    for anything that needs a now's timestamp.
    """
    delta = datetime.now() - datetime.utcfromtimestamp(0)
    return delta.total_seconds()


def get_password_hash(password, salt='THESALTISsaltyLi', rounds=99999):
    """
    used to obtain a users password hash, since password should not be stored in
    the database explicitly this function makes use of the sha512_crypt algorithm
    to make hashes with the default rounds.
    """
    return sha512_crypt.encrypt(password, salt=salt, rounds=rounds)


def get_password_verification(passwordhash, password):
    """
    used when the user is loging in or when the user is attemping to change the
    password. this function should be used by any function that wants to verify
    a user password given a user password hash
    """
    return sha512_crypt.verify(password, passwordhash)


def send_resset_password_email(toemail, fromemail='resetpassword@bootlegtwitter.com'):
    """
    used when the user is loging in or when the user is attemping to change the
    password. this function should be used by any function that wants to verify
    a user password given a user password hash
    """
    subject = 'Password Changed'
    htmlcontent = '<h2>BootlegTwitter Password changed Notification<h2><br>'
    htmlcontent += '<strong>The password for the following account has been changed</strong><br>'
    htmlcontent += '<p>Account: {}</p>'.format(toemail)
    __send_email(fromemail, toemail, subject, htmlcontent)


def send_forgot_password_email(toemail, token, fromemail='forgotpassword@bootlegtwitter.com'):
    """
    used to send account verification email to the user. This function is call only when the user
    needs to reset his/her password after loosing it.
    """
    verification_link = 'http://localhost:5000/set-new-password/'+token
    subject = 'Forgot Password'
    htmlcontent = '<h2>The Following is your Password Reset link From BootlegTwitter:<h2><br>'
    htmlcontent += '<strong>Please Click the following link to Change Your Password</strong><br>'
    htmlcontent += '<a href=\"{}\">Click to Reset password</a>'.format(
        verification_link)
    __send_email(fromemail, toemail, subject, htmlcontent)


def send_account_verification_email(to_email, token, from_email='verifyaccount@bootlegtwitter.com'):
    """
    used to send account verification email to the user. this function is used only once,
    this is when a user is creating an account at BootlegTwitter for the first time.
    """
    verification_link = 'http://localhost:5000/confirm-email/'+token
    subject = 'Account Verification'
    htmlcontent = '<h2>The Following is your account verification link From BootlegTwitter:<h2><br>'
    htmlcontent += '<strong>Please Click the following link to verify your account</strong><br>'
    htmlcontent += '<a href=\"{}\">Click to verify your email address</a>'.format(
        verification_link)
    __send_email(from_email, to_email, subject, htmlcontent)


def __send_email(fromemail, toemail, subject, htmlcontent):
    """
    [private/ helper] function to send emails, to the user at hand. This helper
    function can be used to send account verification, password reset and forgot
    password emails. NOTE: this function is never called directly hence the
    {__send_email} notation.
    """
    msg = Mail(
            from_email=fromemail,
            to_emails=toemail,
            subject=subject,
            html_content=htmlcontent
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(msg)
    except Exception as e:
        print(e)


def validate_password(password):
    """
    uses regular expression to validate password strength at least 9 characters,
    must be restricted to, though does not specifically require any of: uppercase
    letters: A-Z, lowercase letters: a-z, numbers: 0-9 any of the special
    characters: @#$%^&+!=
    """
    return bool(re.match(r'^(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?:.{9,})$', password))


def get_hashtags(rawstring):
    """
    used to obtain/get all the hash tags in a string, used when a user is
    posing a tweet. A hashtag should not be a hashtag if it has special chars
    uses regex to check if a hashtag has special chars. In this case a hash
    tag wont be considered.
    """
    pattern = re.compile(r"#(\w+)")
    return set(pattern.findall(rawstring))


def get_tagged(rawstring):
    """
    used to obtain all the users tagged in a string, used when a user is posing
    a tweet. this assumes that the tagged users are separated by spaces or
    whitespaces and that a tagged user beging with an '@' token or char.
    """
    pattern = re.compile(r"@(\w+)")
    return set(pattern.findall(rawstring))


def validate_date(formInput):
    """ uses regular expression to validate password strength """
    return True


def validate_name(formInput):
    """ uses regular expression to validate password strength """
    return True


def validate_surname(formInput):
    """ sumary_line """
    return True


def validate_string(string):
    """ sumary_line """
    return True


def process_picture(forminput, status):
    """ sumary_line """
    return True


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Test client for models. [NOTE used during development stage]
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':
    print('PASSWORD VALIDATOR ')
    print("Bhesdafsdfasdfki", validate_password("Bhesdafsdfasdfki")) # false
    print("B1jfd!", validate_password("B1jfd!")) # false
    print("B@1jfd!sd", validate_password("B@1jfd!sd"))  # true
    print("Bhek1jhfd#i", validate_password("Bhek1jhfd#i")) #true

    hashtags0 = '#his #cool-kid dhsbhasjbf #cool-kid sadkjfsjkadf kdjsfhakjf\n\
                #kjhf dsakjfh\n dsjkafh dsajfh    hdskjafhjk\t #ndsjfhsd#kjsouthafric'
    hashtags1 = "Hey # guys! #sta3ckoverflow really #rocks #ro_cks #announ!cement"

    tagged0 = "The House of Bonang @seeandbe_seen  30m30 minutes ago More #UthandoNesthembu\
                fuck the matters of the heart I'd marry Musa Mseleku kusizani badikhalisa\
                be poor labo fucken"
    tagged1 = "How One Brand Switched A Million URLs & Lived To Tell About It: 5 Questions\
                With @HomeAdvisor\ http://selnd.com/18WkBZg (@sengineland)"
    tagged2 = "You are like dentures, because I could not smile without you @notseongyeol\
                (@fakepcho91)#FACTS The acid in Coca Cola is called phosphoric acid which\
                is known to dissolve teeth, metal N it can eat away your liver.\
                (@incarceratedbob) Drinking beer actually helps strengthen your bones and\
                teeth because it gives you a healthy dose of silicon. (@UberFacts)"
    print("TAGGED USERS")
    print(get_tagged(tagged0))
    print(get_tagged(tagged1))
    print(get_tagged(tagged2))

    print('HASHTAGS')
    print(get_hashtags(hashtags0))
    print(get_hashtags(hashtags1))

