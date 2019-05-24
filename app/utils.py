#!usr/bin/python
"""
"""
from passlib.hash import sha512_crypt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import date, datetime
from .email_template import *
from textblob import TextBlob
import os
import re

MESSAGE = ''
TYPE = ''

def set_message(message, message_type):
    """
    Sets the globals message and message type
    @params message The message to set to the global buffer
    @params message_type The type of the message for the buffer
    """
    global MESSAGE, TYPE
    MESSAGE = message
    TYPE = message_type


def get_message():
    """
    Sets the globals message to null and return the message
    @return message The message in the global buffer
    """
    global MESSAGE
    msg = MESSAGE
    MESSAGE = ''
    return msg


def get_type():
    """
    Sets the globals message type to null and return the message type
    @return type The message type in the global buffer
    """
    global TYPE
    message_type = TYPE
    TYPE = ''
    return message_type


def get_time_stamp():
    """
    used to get the now's time stamp, this is done when a user is creating a
    post or when the user is creating an account. Essentially this function is
    used for anything that needs a now's timestamp.
    """
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')


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


def send_reset_password_email(toemail, fromemail='resetpassword@twitterLite.com'):
    """
    used when the user is loging in or when the user is attemping to change the
    password. this function should be used by any function that wants to verify
    a user password given a user password hash
    """
    subject = 'Password Changed'
    htmlcontent  = get_reset_password_email_content()
    __send_email(fromemail, toemail, subject, htmlcontent)


def send_forgot_password_email(toemail, token, fromemail='forgotpassword@twitterLite.com'):
    """
    used to send account verification email to the user. This function is call
    only when the user needs to reset his/her password after loosing it.
    """
    verification_link = 'http://localhost:5000/set-new-password/'+token
    subject = 'Forgot Password'
    htmlcontent = get_forgot_password_email_content(verification_link)
    __send_email(fromemail, toemail, subject, htmlcontent)

def send_account_verification_email(to_email, token, from_email='verifyaccount@twitterLite.com'):
    """
    used to send account verification email to the user. this function is used only once,
    this is when a user is creating an account at BootlegTwitter for the first time.
    """
    verification_link = 'http://localhost:5000/confirm-email/'+token
    subject = 'Account Verification'
    htmlcontent = get_verification_email_content(verification_link)
    __send_email(from_email, to_email, subject, htmlcontent)


def __send_email(fromemail, toemail, subject, htmlcontent):
    msg = Mail(
        from_email   = fromemail,
        to_emails    = toemail,
        subject      = subject,
        html_content = htmlcontent
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


def __clean_tweet(rawstring):
    """
    function to clean tweet text by removing links and special characters
    with the aid of regular expression.
    """
    pattern = '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])(\w+:\/\/\S+)'
    return ' '.join(re.sub(pattern, ' ', rawstring).split())


def get_tweet_sentiment(tweet):
    """
    function to classify the sentiment of tweet using TextBlob's sentiment
    polarity method
    """
    analysis = TextBlob(__clean_tweet(tweet))
    if   analysis.sentiment.polarity > 0: return 'positive'
    elif analysis.sentiment.polarity < 0: return 'negative'
    return 'neutral'


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
    tagged0 = "The House of Bonang @seeandbe_seen  30m30 minutes ago More\
                UthandoNesthembu fuck the matters of the heart I'd marry\
                Musa Mseleku kusizani badikhalisa be poor labo fucken"
    tagged1 = "How One Brand Switched A Million URLs & Lived To Tell About\
               It: 5 Questions With @HomeAdvisor\ http://selnd.com/18WkBZg \
               (@sengineland)"
    tagged2 = "You are like dentures, because I could not smile without you \
               @notseongyeol (@fakepcho91)#FACTS The acid in Coca Cola is \
               called phosphoric acid which is known to dissolve teeth, metal\
               N it can eat away your liver.(@incarceratedbob) Drinking beer \
               actually helps strengthen your bones and teeth because it gives\
               you a healthy dose of silicon. (@UberFacts)"

    hashtags0 = '#his #cool-kid dhsbhasjbf #cool-kid sadkjfsjkadf kdjsfhakjf\n\
                #kjhf dsakjfh\n dsjkafh dsajfh    hdskjafhjk\t #ndsjfhsd\
                #kjsouthafric'
    hashtags1 = "Hey # guys! #sta3ckoverflow really #rocks #ro_cks \
                 #announ!cement"

    print(get_tweet_sentiment("Hello I love"))      # positive
    print(get_tweet_sentiment("Hello I Hate"))      # negative
    print(get_tweet_sentiment("Hello I Love/Hate")) # neutral
    print(get_tweet_sentiment(tagged0))
    print(get_tweet_sentiment(tagged1))
    print(get_tweet_sentiment(tagged2))
    print('PASSWORD VALIDATOR ')
    print("Bhesdafsdfasdfki", validate_password("Bhesdafsdfasdfki"))  # false
    print("B1jfd!", validate_password("B1jfd!"))  # false
    print("B@1jfd!sd", validate_password("B@1jfd!sd"))  # true
    print("Bhek1jhfd#i", validate_password("Bhek1jhfd#i"))  # true
    print("TAGGED USERS")
    print(get_tagged(tagged0))
    print(get_tagged(tagged1))
    print(get_tagged(tagged2))
    print('HASHTAGS')
    print(get_hashtags(hashtags0))
    print(get_hashtags(hashtags1))