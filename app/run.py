#!usr/bin/python3

# TODO: All the sectret keys, salts should be placed in a config
from utils import *
from flask import Flask, request, session, redirect, url_for, render_template, flash
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired
from jinja2 import Environment, select_autoescape, FileSystemLoader
from werkzeug.utils import secure_filename
from mock_data import *
from models import *
import os


# TODO: remains in the run.py when moving goes down
app = Flask(__name__)
# TODO: add this to the config file

# TODO: this has to be changed. the salt should be set in a config file

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

salt = URLSafeTimedSerializer(
    'ThisIsASecretSaltStringURLSafeTimedSerializerURLSafeTimedSerializer'
)
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)
UPLOAD_FOLDER                       =   'app/static/img/useravatar/'
ALLOWED_EXTENSIONS                  =   set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER']         =   UPLOAD_FOLDER


def is_logged_in():
    """
    Checks if user is logged in
    @return bool
    """
    return bool(session.get('username'))


@app.route('/',  methods=['GET', 'POST'])
@app.route('/home',  methods=['GET', 'POST'])
def home():
    if is_logged_in() == False:
        return redirect('/login', '302')

    user = User(session['username'])
    return render_template(
        'index.html',
        user=user.get_json_user(),
        tweets=mock_tweets,
        treading=mock_treading,
        account=True,
        fsuggestions=mock_fsuggestions
    )


@app.route('/login', methods=['GET', 'POST'])
@app.route('/signin', methods=['GET', 'POST'])
def login():
    """ sumary_line """
    # Redirect User if the user is logged already
    if is_logged_in():
        return redirect('/', 302)
    if request.method == 'POST':
        # TODO: user regualr expression to validate user input
        username = request.form['username']
        password = request.form['password']
        user = User(username)
        login_status = user.user_login(password)
        if login_status == -1:
            return ('Invalid user account please check your username.')
        elif login_status == -2:
            return ('Account not verified, please check you email to verify account.')
        elif login_status == True:
            session['username'] = username
            return redirect('/', 302)
        elif login_status == False:
            return ('Wrong password, please check your password or change it if you forgot the password.')

    template = env.get_template("login.html")
    return template.render()


@app.route('/friends')
def friends():
    """ sumary_line """
    template = env.get_template("friends.html")
    user = User(session['username']).get_json_user()
    return template.render(
        user=user,
        tweets=mock_tweets,
        treading=mock_treading,
        fsuggestions=mock_fsuggestions,
        following=mock_following,
        followers=mock_followers,
        personaltweets=mock_personal
    )


@app.route('/about')
def about():
    """ sumary_line """
    template = env.get_template("about.html")
    return template.render()


@app.route('/account')
def account():
    """ sumary_line """
    try:
        template = env.get_template("account.html")
        user = User(session['username']).get_json_user()
        return template.render(
            user=user,
            tweets=mock_tweets,
            treading=mock_treading,
            fsuggestions=mock_fsuggestions
        )
    except KeyError:
        return render_template('login.html')


@app.route('/messages')
def messages():
    """ sumary_line """
    template = env.get_template("messages.html")
    user = User(session['username']).get_json_user()
    return template.render(
        user=user,
        tweets=mock_tweets,
        treading=mock_treading,
        messages=mock_messages,
        fsuggestions=mock_fsuggestions
    )


# TODO: Must implement - Get user data from db
@app.route('/profile/<username>')
def view_user_bio(username):
    """ sumary_line """
    template = env.get_template("friends.html")

    user, vuser  = User(username), User(session['username'])

    following  = [User(uname).get_json_user() for uname in user.get_user_following()]
    vfollowing = [User(uname).get_json_user() for uname in vuser.get_user_following()]
    followers  = [User(uname).get_json_user() for uname in user.get_user_followers()]
    tweets     = [user.get_json_post(tweetid) for tweetid in user.get_user_posts()]

    activeunfollowbtn = True if session['username'] == username else False
    for f in followers:
        f['following'] = f in vfollowing or f['username'] == session['username']

    return template.render(
        user=user.get_json_user(),
        tweets=mock_tweets,
        treading=mock_treading,
        fsuggestions=mock_fsuggestions,
        following=following,
        followers=followers,
        personaltweets=tweets,
        activeunfollowbtn=activeunfollowbtn
    )


@app.route('/logout')
def logout():
    """
    functionality used to log out/ sigout a user, the existing session token/
    id attached to the user is deleted.
    """
    session.pop('username', None)
    flash('Logged out.')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    """ sumary_line """
    if request.method == 'POST':
        # TODO: user regualr expression to validate user input
        email = request.form['email']
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dob = request.form['dob']
        gender = request.form['gender']
        password0 = request.form['password']
        password1 = request.form['password1']
        if password0 != password1:
            return ('passwords do not match')
        if not validate_password(password0):
            return ('Password should be at least 9 chars, A-Za-z0-9 with atleast one special char.')
        user = User(username)
        if not user.get_this_user_data():
            user.add_user(firstname, lastname, email, dob,
                        gender, get_password_hash(password0))
            token = salt.dumps(username, salt='email-confirm')
            send_account_verification_email(email, token)
            return ('a verification Email Has been sent please check you email inbox')
        else:
            return ('This username already exits please select a new user name')
    template = env.get_template("register.html")
    return template.render()


@app.route('/post', methods=['POST'])
def add_tweet():
    if request.method == 'POST' and is_logged_in():
        tweet = request.form['tweet']
        hashtags, taggedusers = get_hashtags(tweet),  get_tagged(tweet)
        user = User(session['username']).add_post(tweet, hashtags, taggedusers)
        return '<h1>Post posted<h1>'


@app.route('/verify-email/<token>')
@app.route('/confirm-email/<token>')
def confirm_email(token):
    """ sumary_line """
    try:
        username = salt.loads(token, salt='email-confirm', max_age=3600)
        user = User(username)
        user.verify_user_account()
        email = user.get_user_email()
        return '<h1>Email: {} has been verified</h1>'.format(email)
    except SignatureExpired:
        flash('This token has expired')


@app.route('/password', methods=['GET', 'POST'])
def forgot_password():
    """
    sumary_line
    """
    if request.method == 'POST':
        pass
    template = env.get_template("forgot-password.html")
    return template.render()


@app.route('/update-user-profile', methods=['POST'])
def update_user_profile():
    """
    sumary_line
    """
    if request.method == 'POST' and is_logged_in():
        newlastname  = request.form['lastname']
        newfirstname = request.form['firstname']
        newdob       = request.form['dob']
        newtitle     = request.form['title']
        newbio       = request.form['bio']

        user = User(session['username'])
        user.update_user_bio(newbio)
        user.update_user_title(newtitle)
        user.update_user_dob(newdob)
        user.update_user_firstname(newfirstname)
        user.update_user_lastname(newlastname)
        f = request.files['avatar']
        filepath = os.path.abspath("../"+UPLOAD_FOLDER+f.filename)
        # this is not safe in practise you need to secure the file before an upload
        f.save(filepath)
        user.update_user_avatar('/static/img/useravatar/'+f.filename)
        return 'Your Details have been updated.'
    return render_template('account.html')


@app.route('/set-new-password', methods=['POST'])
def set_new_password():
    """
    doc-string
    """
    if request.method == 'POST' and is_logged_in():
        if request.form['newpassword0'] == request.form['newpassword1']:
            if validate_password(request.form['newpassword0']):
                oldpassword = request.form['oldpassword']
                user = User(session['username'])
                if get_password_verification(user.get_password_hash(), oldpassword):
                    newpasswordhash = get_password_hash(request.form['newpassword1'])
                    user.update_password_hash(newpasswordhash)
                    send_resset_password_email(user.get_user_email())
                    return ('Password updated.')
                return ('Wrong password, please try again.')
            return ('Password should be at least 9 chars, A-Za-z0-9 with atleast one special char.')
        return ('Password do not match, please try again.')
    return render_template('account.html')


@app.route('/search', methods=['POST'])
def search_user():
    """
    doc - string
    """
    if request.method == 'POST' and is_logged_in():
        user = User(request.form['search'])
        useravailability = user.get_this_user_data()
        if bool(useravailability):
            user = user.get_json_user()
            return view_user_bio(request.form['search']) # return the user profile page with an option of following
        return " user not found"
    return "nothing"


@app.route('/like/<postid>', methods=['GET'])
def like_post(postid):
    """
    Likes a users post
    @params postid Postid of the post to like
    """
    if request.method == 'GET':
        if False == is_logged_in():
            flash('Login to like a post')
            return render_template('login.html')
        User(session['username']).like_post(postid)
        flash('Liked post.')
        return 'liked post' # this should be a template


@app.route('/retweet/<postid>', methods=['GET'])
def retweet_post(postid):
    """
    used to retweet a tweet
    """
    if False == is_logged_in():
        flash('Login to retweet a post')
        return render_template('login.html')
    User(session['username']).retweet_post(postid)
    flash('retweed post')
    return 'retweed post' # this should be a template


@app.route('/follow/<username>', methods=['GET'])
def follow_user(username):
    """
    Follows a user
    @params username Username of the user to follow
    """
    if False == is_logged_in():
        flash('Login to like a post')
        return render_template('login.html')
    User(session['username']).follow_user(username)
    flash('Following user')
    return 'followed user' # this should be a template


if __name__ == '__main__':
    app.run(debug=True)