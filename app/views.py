#!usr/bin/python3
from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify
from itsdangerous import URLSafeSerializer
from itsdangerous.exc import BadSignature
from jinja2 import Environment, select_autoescape, FileSystemLoader
from werkzeug.utils import secure_filename
from .models import *
from .utils import *
# from nltk_model import *
import os

app                         = Flask(__name__)
UPLOAD_FOLDER               = '/static/img/useravatar/'
ALLOWED_EXTENSIONS          = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/profile/<username>')
def view_user_bio(username):
    """ sumary_line """
    if bool(session.get('username')) == False:
        set_message("Please Login", "danger")
        return redirect('/login', '302')

    if username == session['username']:
        user      = session_user      = User(username)
        following = vfollowing        = user.get_user_following()
        user_data = session_user_data = user.get_user_details()
    else:
        user = User(username)
        session_user = User(session['username'])
        user_data = user.get_user_details()
        session_user_data = session_user.get_user_details()
        following = user.get_user_following()
        vfollowing = session_user.get_user_following()

    followers          = user.get_user_followers()
    tweets             = user.get_user_posts()
    activeunfollow     = True if session['username'] == username else False
    unfollowthisuser   = session_user.is_following(username)
    friend_suggestions = session_user.get_recommended_users()
    trending           = get_trending_hashtags_for_user(session['username'])

    for tweet in tweets:
        tweet['likers'] = get_tweet_likes_usernames(tweet['id'])
        tweet['retweeters'] = get_tweet_retweets_usernames(tweet['id'])
        tweet['likebtnactive'] = session['username'] in tweet['likers']
        tweet['retweetbtnactive'] = session['username'] in tweet['retweeters']

    # deactivate unfollow button for me while viewing a guest account
    for f in followers:
        f['following'] = f in vfollowing or f['username'] == session['username']

    return render_template(
        "friends.html",
        session_user     = session_user_data,
        user             = user_data,
        treading         = trending,
        fsuggestions     = friend_suggestions,
        following        = following,
        followers        = followers,
        personaltweets   = tweets,
        activeunfollow   = activeunfollow,
        unfollowthisuser = unfollowthisuser
    )


@app.route('/',  methods=['GET', 'POST'])
def home():
    if bool(session.get('username')) == False:
        set_message("Please Login", "danger")
        return redirect('/login', 302)

    # Must always be there
    session_user = User(session['username'])

    # if not visiting another persons profile
    user_details = session_user.get_user_details()
    trending = get_trending_hashtags_for_user(session['username'])
    tweets = session_user.get_timeline_posts()
    # train_data = train_model("train8.csv")

    for tweet in tweets:
        tweet[1]['likers'] = get_tweet_likes_usernames(tweet[1]['id'])
        tweet[1]['retweeters'] = get_tweet_retweets_usernames(tweet[1]['id'])
        tweet[1]['likebtnactive'] = session['username'] in tweet[1]['likers']
        tweet[1]['retweetbtnactive'] = session['username'] in tweet[1]['retweeters']
        # tweet[1]['topic'] = get_topics(tweet[1]['tweet'], "train_data")

    return render_template(
        'index.html',
        session_user = user_details,
        user         = user_details,
        tweets       = tweets,
        treading     = trending,
        fsuggestions = session_user.get_recommended_users(),
        message      = get_message(),
        alert        = get_type()
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ sumary_line """
    # Redirect User if the user is logged already
    if bool(session.get('username')):
        set_message('User already Logged in', 'warning')
        return redirect('/', 302)
    if request.method == 'POST':
        # TODO: user regualr expression to validate user input
        username = request.form['username']
        password = request.form['password']
        login_status = User(username).user_login(password)
        if login_status == -1:
            set_message('Invalid username check your username', 'danger')
        elif login_status == -2:
            set_message('Account not verified, check your email', 'warning')
        elif login_status == False:
            set_message('Wrong password, try signing in again', 'danger')
        elif login_status == True:
            session['username'] = username
            return redirect('/', 302)
        return redirect('/login', 302)
    message, alert = get_message(), get_type()
    return render_template('login.html', message=message, alert=alert)


@app.route('/account')
def account():
    """ sumary_line """
    if bool(session.get('username')) == False:
        set_message("Please Login", "danger")
        return redirect('/login', '302')

    user = User(session['username'])
    user_data = user.get_user_details()
    return render_template(
        "account.html",
        session_user = user_data,
        user         = user_data,
        tweets       = user.get_timeline_posts(),
        treading     = get_trending_hashtags_for_user(session['username']),
        fsuggestions = user.get_recommended_users(),
        message      = get_message(),
        alert        = get_type()
    )


@app.route('/tag/<hashtag>')
def tag(hashtag):
    """
    Gets the top 5 trendiing hashtags from a users followers
    @params user the username of the user
    """
    if bool(session.get('username')) == False:
        set_message("Please Login to like tweets", "danger")
        return redirect('/login', '302')

    # Must always be there
    user = User(session['username'])
    user_data = user.get_user_details()
    tweets = get_tweets_by_hashtag(session['username'], hashtag)
    friend_suggestions = user.get_recommended_users()
    trending_hashtags = get_trending_hashtags_for_user(session['username'])

    msg = get_message()
    alert = get_type()
    if not tweets:
    	return render_template(
            'hashtag_no_tweets.html',
            session_user = user_data,
            user         = user_data,
            tweets       = tweets,
            treading     = trending_hashtags,
            fsuggestions = friend_suggestions,
            message      = msg,
            alert        = alert
        )
    for tweet in tweets:
        tweet[1]['likers'] = get_tweet_likes_usernames(tweet[1]['id'])
        tweet[1]['retweeters'] = get_tweet_retweets_usernames(tweet[1]['id'])
        tweet[1]['likebtnactive'] = session['username'] in tweet[1]['likers']
        tweet[1]['retweetbtnactive'] = session['username'] in tweet[1]['retweeters']

    return render_template(
        'hashtag_search.html',
        session_user = user_data,
        user         = user_data,
        tweets       = tweets,
        treading     = trending_hashtags,
        fsuggestions = friend_suggestions,
        message      = msg,
        alert        = alert
    )


@app.route('/logout')
def logout():
    """
    functionality used to log out/ sigout a user, the existing session token/
    id attached to the user is deleted.
    """
    if bool(session.get('username')) == False:
        set_message("This Session does not exist", "danger")
        return redirect('/login', 302)

    session.pop('username', None)
    set_message('Logged out', 'primary')
    return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def register():
    """ sumary_line """
    if request.method == 'POST':
        # TODO: user regualr expression to validate user input
        email     = request.form['email']
        username  = request.form['username']
        firstname = request.form['firstname']
        lastname  = request.form['lastname']
        dob       = request.form['dob']
        gender    = request.form['gender']
        password0 = request.form['password']
        password1 = request.form['password1']
        if password0 != password1:
            set_message('passwords do not match', 'danger')
            return redirect('/register', 302)
        elif not validate_password(password0):
            set_message(
                'Password should be at least 9 chars, [A-Za-z0-9@#$%^&+!=.]',
                'warning'
            )
            return redirect('/register', 302)
        user = User(username)
        if not user.get_user_details():
            user.add_user(
                firstname,
                lastname,
                email,
                dob,
                gender,
                get_password_hash(password0)
            )
            urlsafeserializer = URLSafeSerializer(os.environ.get('SALT'))
            token = urlsafeserializer.dumps(username, salt='email-confirm')
            send_account_verification_email(email, token)
            set_message(
                'a verification Email Has been sent please check you email inbox',
                'success'
            )
            return redirect('/login', 302)
        else:
            set_message(
                'This username already exits please select a new user name',
                'warning'
            )
            return redirect('/register', 302)
    return render_template("register.html")


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """
    sumary_line
    """
    message, alert = '', ''
    if request.method == 'POST':
        username = request.form['username']
        user = User(username).get_user_details()
        if bool(user):
            email = user['useremail']
            urlsafeserializer = URLSafeSerializer(os.environ.get('SALT'))
            token = urlsafeserializer.dumps(username, salt='forgot-password')
            send_forgot_password_email(email, token)
            message = 'password reset email sent to: {0} does not exit'.format(email)
            alert = 'danger'
        message = 'username: {0} does not exit'.format(username)
        alert = 'danger'
    return render_template('forgot-password.html', message=message, alert=alert)

@app.route('/set-new-password/<token>')
def reset_password(token):
    """ sumary_line """
    try:
        urlsafeserializer = URLSafeSerializer(os.environ.get('SALT'))
        username = urlsafeserializer.loads(token, salt='forgot-password')
        if request.form['newpassword0'] == request.form['newpassword1']:
            if validate_password(request.form['newpassword0']):
                user = User(username)
                newpasswordhash = get_password_hash(request.form['newpassword1'])
                user.update_password_hash(newpasswordhash)
                send_reset_password_email(user.get_user_email())
                message = 'Password updated'
                alert = 'success'
                return render_template('/login.html', message=message, alert=alert)
            message = 'Password should be at least 9 chars, [A-Za-z0-9@#$%^&+!=.]'
            alert = 'warning'
            return '<h3>'+ message + ' ' + alert +'</h3>'
        message = 'passwords do not match'
        alert = 'danger'
        return '<h3>'+ message + ' '+ alert +'</h3>'

    except BadSignature:
        message = 'This token has been tempered with create a new account'
        alert = 'danger'
        return redirect('/login', 302)

@app.route('/confirm-email/<token>')
def confirm_email(token):
    """ sumary_line """
    try:
        urlsafeserializer = URLSafeSerializer(os.environ.get('SALT'))
        username = urlsafeserializer.loads(token, salt='email-confirm')
        User(username).verify_user_account()
        set_message('Account Verified, Login to start Tweeting', 'primary')
    except BadSignature:
        set_message(
            'This token has been tempered with create a new account',
            'danger'
        )
    return redirect('/login', 302)


@app.route('/update-user-profile', methods=['POST'])
def update_user_profile():
    """
    used to update the use profile credentials. if no values are renewed this
    still updates the database with the update user account form default values
    which in this case are the users currant credentials.
    """
    if request.method == 'POST' and bool(session.get('username')):
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
        filepath = os.path.abspath(UPLOAD_FOLDER+f.filename)
        # this is not safe in practise you need to secure the file
        # before an upload
        f.save(filepath)
        user.update_user_avatar('/static/img/useravatar/'+f.filename)
        return 'Your Details have been updated.'
    return render_template('account.html')


@app.route('/set-new-password', methods=['POST'])
def set_new_password():
    """
    used to set a new password in the user account settings section
    this updates the user password hash which is stored in the database
    """
    if bool(session.get('username')) == False:
        set_message("Please Login", "danger")
        return redirect('/login', 302)
    if request.method == 'POST':
        if request.form['newpassword0'] == request.form['newpassword1']:
            if validate_password(request.form['newpassword0']):
                oldpassword = request.form['oldpassword']
                user = User(session['username'])
                if get_password_verification(user.get_password_hash(), oldpassword):
                    newpasswordhash = get_password_hash(request.form['newpassword1'])
                    user.update_password_hash(newpasswordhash)
                    send_reset_password_email(user.get_user_email())
                    set_message("Password updated", "primary")
                set_message('Wrong password, please try again.', 'warning')
            set_message(
                'Password should be at least 9 chars, [A-Za-z0-9@#$%^&+!=.]',
                'warning'
            )
        set_message('Passwords do not match, try again.', 'warning')
    return redirect('/account', 302)


@app.route('/search/<string>', methods=['GET'])
def search(string):
    """
    used for searching the database for users that match the {string}
    this uses a substring search to achieve the outcome
    """
    if bool(session.get('username')) == False:
        set_message("Please Login", "danger")
        return redirect('/login', 302)
    return jsonify(username=search_users(string))


@app.route('/likers/<postid>', methods=['GET'])
def get_likers(postid):
    """
    Likes a users post
    @params postid Postid of the post to like
    """
    if bool(session.get('username')) == False:
        set_message("Please Login", "danger")
        return redirect('/login', 302)
    return jsonify(users=get_tweet_likes_usernames(postid))


@app.route('/retweeters/<postid>', methods=['GET'])
def get_retweeters(postid):
    """
    used to obtain the usernames of users that have retweeted a post
    """
    if False == bool(session.get('username')):
        set_message("Please Login", "danger")
        return redirect('/login', 302)
    return jsonify(users=get_tweet_retweets_usernames(postid))


@app.route('/follow/<username>', methods=['GET'])
def follow_user(username):
    """
    follow a user
    @params username Username of the user to follow
    """
    if False == bool(session.get('username')):
        set_message("you should be loged in to follow a user", "danger")
        return redirect('/login', 302)
    User(session['username']).follow_user(username)
    return 'Unfollow'


@app.route('/unfollow/<username>', methods=['GET'])
def unfollow_user(username):
    """
    Unfollow a user
    @params username Username of the user to follow
    """
    if False == bool(session.get('username')):
        set_message("you should be logged in to unfollow a user", "danger")
        return redirect('/login', 302)
    User(session['username']).unfollow_user(username)
    return 'Follow'


@app.route('/retweet/<postid>', methods=['GET'])
def retweet_post(postid):
    """
    used to retweet a tweet
    @params postid Postid of the post to retweet
    """
    if False == bool(session.get('username')):
        set_message("Login to retweet a post", "danger")
        return redirect('/login', 302)
    User(session['username']).retweet_post(postid)
    return 'Unretweet'


@app.route('/post', methods=['POST'])
def add_tweet():
    if bool(session.get('username')) == False:
        set_message("Please Login to post", "danger")
        return redirect('/login', 302)
    if request.method == 'POST' and bool(session.get('username')):
        tweet = request.form['tweet']
        hashtags, taggedusers = get_hashtags(tweet),  get_tagged(tweet)
        User(session['username']).add_post(tweet, hashtags, taggedusers)
        set_message('Post posted', 'primary')
    return redirect('/', 302)


@app.route('/unretweet/<postid>', methods=['GET'])
def unretweet_post(postid):
    """
    used to unretweet a tweet
    @params postid Postid of the post to unretweet
    """
    if False == bool(session.get('username')):
        set_message("Login to retweet a post", "danger")
        return redirect('/login', 302)
    User(session['username']).unretweet_tweet(postid)
    return 'Retweet'


@app.route('/like/<postid>', methods=['GET'])
def like_post(postid):
    """
    like a users post
    @params postid Postid of the post to like
    """
    if bool(session.get('username')) == False:
        set_message("Please Login to like tweets", "danger")
        return redirect('/login', '302')
    User(session['username']).like_post(postid)
    return "Unlike"


@app.route('/unlike/<postid>', methods=['GET'])
def unlike_post(postid):
    """
    unlike a users post
    @params postid Postid of the post to unlike
    """
    if bool(session.get('username')) == False:
        set_message("Please Login to like tweets", "danger")
        return redirect('/login', 302)
    User(session['username']).unlike_tweet(postid)
    return 'Like'


@app.route('/usernetwork', methods=['GET'])
def usernetwork():
    """
    used for the tab that enables the visualisation of a D3js visualization of
    application wide user network of users, with follow relationships indicated,
    and each user also labelled by username and total number of likes of tweets
    """
    if bool(session.get('username')) == False:
        set_message("Please Login", "danger")
        return redirect('/login', 302)

    dump_user_network()
    session_user_data = User(session['username']).get_user_details()
    return render_template(
        "user-networkD3.html",
        session_user = session_user_data,
        user         = session_user_data
    )