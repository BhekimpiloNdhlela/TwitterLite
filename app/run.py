#!usr/bin/python3
from utils import *
from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired
from jinja2 import Environment, select_autoescape, FileSystemLoader
from werkzeug.utils import secure_filename
from mock_data import *
from models import *
from nltk_model import *
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
salt = URLSafeTimedSerializer(os.environ.get('SALT'))

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)
UPLOAD_FOLDER = 'app/static/img/useravatar/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def is_logged_in():
    """
    Checks if user is logged in
    @return bool True if logged in and false if not
    """
    return bool(session.get('username'))


@app.route('/profile/<username>')
def view_user_bio(username):
    """ sumary_line """
    if is_logged_in() == False:
        set_message("Please Login", "danger")
        return redirect('/login', '302')

    template = env.get_template("friends.html")

    user, session_user = User(username), User(session['username'])
    following = user.get_user_following()
    vfollowing = session_user.get_user_following()
    followers = user.get_user_followers()

    tweets = user.get_user_posts()
    for tweet in tweets:
        tweet['likers'] = get_tweet_likes_usernames(tweet['id'])
        tweet['retweeters'] = get_tweet_retweets_usernames(tweet['id'])

    activeunfollow = True if session['username'] == username else False

    for f in followers:
        f['following'] = f in vfollowing or f['username'] == session['username']

    friend_suggestions = session_user.get_recommended_users()

    return template.render(
        session_user=session_user.get_json_user(),
        user=user.get_json_user(),
        tweets=mock_tweets,
        treading=mock_treading,
        fsuggestions=friend_suggestions,
        following=following,
        followers=followers,
        personaltweets=tweets,
        activeunfollow=activeunfollow
    )


@app.route('/',  methods=['GET', 'POST'])
@app.route('/home',  methods=['GET', 'POST'])
def home():
    if is_logged_in() == False:
        set_message("Please Login", "danger")
        return redirect('/login', '302')

    # Must always be there
    session_user = User(session['username'])

    # if not visiting another persons profile
    user = session_user.get_json_user()
    tweets = session_user.get_timeline_posts()
    for tweet in tweets:
        tweet[1]['likers'] = get_tweet_likes_usernames(tweet[1]['id'])
        tweet[1]['retweeters'] = get_tweet_retweets_usernames(tweet[1]['id'])
    friend_suggestions = session_user.get_recommended_users()

    msg = get_message()
    alert = get_type()

    return render_template(
        'index.html',
        session_user=session_user.get_json_user(),
        user=user,
        tweets=tweets,
        treading=mock_treading,
        fsuggestions=friend_suggestions,
        message=msg,
        alert=alert
    )


@app.route('/login', methods=['GET', 'POST'])
@app.route('/signin', methods=['GET', 'POST'])
def login():
    """ sumary_line """
    # Redirect User if the user is logged already
    if is_logged_in():
        set_message("Please Login", "danger")
        return redirect('/', 302)
    if request.method == 'POST':
        # TODO: user regualr expression to validate user input
        username = request.form['username']
        password = request.form['password']
        user = User(username)
        login_status = user.user_login(password)
        if login_status == -1:
            set_message(
                'Invalid user account please check your username', 'danger')
        elif login_status == -2:
            set_message(
                'Account not verified, please check your email', 'warning')
        elif login_status == False:
            set_message(
                'Wrong password, Please try signing in again.', 'danger')
        elif login_status == True:
            session['username'] = username
            return redirect('/', 302)
    return render_template('login.html', message=get_message(), alert=get_type())


@app.route('/about')
def about():
    """ sumary_line """
    template = env.get_template("about.html")
    return template.render()


@app.route('/account')
def account():
    """ sumary_line """
    if is_logged_in() == False:
        return redirect('/login', '302')

    template = env.get_template("account.html")
    session_user = User(session['username'])
    user = session_user.get_json_user()
    tweets = session_user.get_timeline_posts()
    friend_suggestions = session_user.get_recommended_users()

    user_tweets = [session_user.get_user_posts()]

    train_data = train_model("train.csv")
    topics = []
    test_tweet = "This tweet about weather and the solar eclipse"
    # for tweet in tweets:
    topics.append(get_topics(test_tweet, train_data))

    return template.render(
        session_user=session_user.get_json_user(),
        user=user,
        tweets=tweets,
        topics=topics,
        treading=mock_treading,
        fsuggestions=friend_suggestions,
        message=get_message(),
        alert=get_type()
    )


@app.route('/tag')
def tag():
    template = env.get_template("tag.html")
    user = User(session['username']).get_json_user()
    return template.render(
        user=user,
        tweets=mock_tweets,
        treading=mock_treading,
        messages=mock_messages,
        fsuggestions=mock_fsuggestions
    )


@app.route('/messages')
def messages():
    """ sumary_line """
    if is_logged_in() == False:
        set_message('Please Login', 'danger')
        return redirect('/login', '302')

    template = env.get_template("messages.html")
    session_user = User(session['username'])
    user = session_user.get_json_user()
    tweets = session_user.get_timeline_posts()
    friend_suggestions = session_user.get_recommended_users()
    return template.render(
        session_user=session_user.get_json_user(),
        user=user,
        treading=mock_treading,
        messages=mock_messages,
        fsuggestions=friend_suggestions
    )


@app.route('/logout')
def logout():
    """
    functionality used to log out/ sigout a user, the existing session token/
    id attached to the user is deleted.
    """
    session.pop('username', None)
    set_message('Logged out', 'primary')
    return redirect('/login')


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
            user.add_user(
                firstname,
                lastname,
                email,
                dob,
                gender,
                get_password_hash(password0)
            )
            token = salt.dumps(username, salt='email-confirm')
            send_account_verification_email(email, token)
            return ('a verification Email Has been sent please check you email inbox')
        else:
            return ('This username already exits please select a new user name')
    template = env.get_template("register.html")
    return template.render()


@app.route('/post', methods=['POST'])
def add_tweet():
    if is_logged_in() == False:
        set_message("Please Login to post", "danger")
        return redirect('/login', '302')
    if request.method == 'POST' and is_logged_in():
        tweet = request.form['tweet']
        hashtags, taggedusers = get_hashtags(tweet),  get_tagged(tweet)
        User(session['username']).add_post(tweet, hashtags, taggedusers)
        set_message('Post posted', 'primary')
    return redirect('/', '302')


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
        newlastname = request.form['lastname']
        newfirstname = request.form['firstname']
        newdob = request.form['dob']
        newtitle = request.form['title']
        newbio = request.form['bio']

        user = User(session['username'])
        user.update_user_details(
            newfirstname,
            newlastname,
            newdob,
            newtitle,
            newbio
        )
        f = request.files['avatar']
        filepath = os.path.abspath("../"+UPLOAD_FOLDER+f.filename)
        # this is not safe in practise you need to secure the file
        # before an upload
        f.save(filepath)
        user.update_user_avatar('/static/img/useravatar/'+f.filename)
        return 'Your Details have been updated.'
    return render_template('account.html')


@app.route('/set-new-password', methods=['POST'])
def set_new_password():
    """
    doc-string
    """
    if is_logged_in() == False:
        set_message("Please Login", "danger")
        return redirect('/login', '302')
    if request.method == 'POST':
        if request.form['newpassword0'] == request.form['newpassword1']:
            if validate_password(request.form['newpassword0']):
                oldpassword = request.form['oldpassword']
                user = User(session['username'])
                if get_password_verification(user.get_password_hash(), oldpassword):
                    newpasswordhash = get_password_hash(
                        request.form['newpassword1'])
                    user.update_password_hash(newpasswordhash)
                    send_resset_password_email(user.get_user_email())
                    set_message("Password updated", "primary")
                    return redirect('/account', '302')
                set_message('Wrong password, please try again.', 'warning')
                return redirect('/account', '302')
            set_message(
                'Password should be at least 9 chars, [A-Za-z0-9@#$%^&+!=.]', 'warning')
            return redirect('/account', '302')
        set_message('Password do not match, please try again.', 'warning')
    return redirect('/account', '302')


@app.route('/search', methods=['POST'])
def search_user():
    """
    doc - string
    """
    if is_logged_in() == False:
        set_message("Please Login", "danger")
        return redirect('/login', '302')

    if request.method == 'POST':
        user = User(request.form['search'])
        useravailability = user.get_this_user_data()
        if bool(useravailability):
            user = user.get_json_user()
            # return the user profile page with an option of following
            return view_user_bio(request.form['search'])
        return "user not found"
    return "nothing"


@app.route('/like/<postid>', methods=['GET'])
def like_post(postid):
    """
    Likes a users post
    @params postid Postid of the post to like
    """
    if is_logged_in() == False:
        set_message("Please Login to like tweets", "danger")
        return redirect('/login', '302')
    if request.method == 'GET':
        User(session['username']).like_post(postid)
        return 'Unliked'  # this should be a template


@app.route('/likers/<postid>', methods=['GET'])
def get_likers(postid):
    """
    Likes a users post
    @params postid Postid of the post to like
    """
    if is_logged_in() == False:
        set_message("Please Login", "danger")
        return redirect('/login', '302')

    if request.method == 'GET':
        return jsonify(users=get_tweet_likes_usernames(postid))


@app.route('/retweet/<postid>', methods=['GET'])
def retweet_post(postid):
    """
    used to retweet a tweet
    """
    if False == is_logged_in():
        set_message("Login to retweet a post", "danger")
        return redirect('/login', 302)
    User(session['username']).retweet_post(postid)
    return 'True'  # this should be a template


@app.route('/retweeters/<postid>', methods=['GET'])
def get_retweeters(postid):
    if request.method == 'GET':
        if False == is_logged_in():
            flash('Login to retweet a post')
            return render_template('login.html')
        return jsonify(users=get_tweet_retweets_usernames(postid))


@app.route('/follow/<username>', methods=['GET'])
def follow_user(username):
    """
    Follows a user
    @params username Username of the user to follow
    """
    if False == is_logged_in():
        set_message("Login to follow a user", "danger")
        return redirect('/login', 302)

    User(session['username']).follow_user(username)
    return 'Unfollow'


if __name__ == '__main__':
    app.run(debug=True)
