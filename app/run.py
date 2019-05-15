#!usr/bin/python3
from utils import *
from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired
from jinja2 import Environment, select_autoescape, FileSystemLoader
from werkzeug.utils import secure_filename
from mock_data import *
from models import *
# from nltk_model import *
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
    # NOTE: KINDA SHITY WAY OF DOING IT FIX THIS
    if username == session['username']:
        user = session_user = User(username)
    else:
        user, session_user = User(username), User(session['username'])

    following = user.get_user_following()
    vfollowing = session_user.get_user_following()
    followers = user.get_user_followers()
    tweets = user.get_user_posts()
    activeunfollow = True if session['username'] == username else False
    unfollowthisuser = session_user.is_following(username)
    friend_suggestions = session_user.get_recommended_users()

    for tweet in tweets:
        tweet['likers'] = get_tweet_likes_usernames(tweet['id'])
        tweet['retweeters'] = get_tweet_retweets_usernames(tweet['id'])
        tweet['likebtnactive'] = session['username'] in tweet['likers']
        tweet['retweetbtnactive'] = session['username'] in tweet['retweeters']

    # deactivate unfollow button for me while viewing a guest account
    for f in followers:
        f['following'] = f in vfollowing or f['username'] == session['username']
    return template.render(
        session_user=session_user.get_json_user(),
        user=user.get_json_user(),
        tweets=mock_tweets,
        treading=mock_treading,
        fsuggestions=friend_suggestions,
        following=following,
        followers=followers,
        personaltweets=tweets,
        activeunfollow=activeunfollow,
        unfollowthisuser=unfollowthisuser
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
    # train_data = train_model("train8.csv")

    for tweet in tweets:
        tweet[1]['likers'] = get_tweet_likes_usernames(tweet[1]['id'])
        tweet[1]['retweeters'] = get_tweet_retweets_usernames(tweet[1]['id'])
        tweet[1]['likebtnactive'] = session['username'] in tweet[1]['likers']
        tweet[1]['retweetbtnactive'] = session['username'] in tweet[1]['retweeters']
        # tweet[1]['topic'] = get_topics(tweet[1]['tweet'], train_data)

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

    user_tweets = session_user.get_user_posts()

    """
    TODO: uncomment the analytics code after Keanu freezes to the dependency file
    """
    # train_data = train_model("train.csv")
    # topics = []
    # # test_tweet = "This tweet about weather and the solar eclipse"
    # for tweet in user_tweets:
    #     topics.append(get_topics(tweet['tweet'], train_data))

    return template.render(
        session_user=session_user.get_json_user(),
        user=user,
        tweets=tweets,
        # topics=topics,
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
        fsuggestions=mock_fsuggestions
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
            set_message(
                'a verification Email Has been sent please check you email inbox', 'success')
            return redirect('/login', '302')
        else:
            set_message(
                'This username already exits please select a new user name', 'warning')
            return redirect('/register', '302')
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
        # TODO: forgot password functionality
        pass
    template = env.get_template("forgot-password.html")
    return template.render()


@app.route('/update-user-profile', methods=['POST'])
def update_user_profile():
    """
    used to update the use profile credentials. if no values are renewed this
    still updates the database with the update user account form default values
    which in this case are the users currant credentials.
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
    used to set a new password in the user account settings section
    this updates the user password hash which is stored in the database
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
    used for searching for a user from the database. this should be a valid user name
    or a user not found message will be displayed
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


@app.route('/search/<string>', methods=['GET'])
def search(string):
    """
    used for searching the database for users that match the {string}
    this uses a substring search to achieve the outcome
    """
    return jsonify(username=search_users(string))


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


@app.route('/retweeters/<postid>', methods=['GET'])
def get_retweeters(postid):
    """
    used to obtain the usernames of users that have retweeted a post
    """
    if request.method == 'GET':
        if False == is_logged_in():
            flash('Login to retweet a post')
            return render_template('login.html')
        return jsonify(users=get_tweet_retweets_usernames(postid))


@app.route('/follow/<username>', methods=['GET'])
def follow_user(username):
    """
    follow a user
    @params username Username of the user to follow
    """
    if False == is_logged_in():
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
    if False == is_logged_in():
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
    if False == is_logged_in():
        set_message("Login to retweet a post", "danger")
        return redirect('/login', 302)
    User(session['username']).retweet_post(postid)
    return 'Unretweet'


@app.route('/unretweet/<postid>', methods=['GET'])
def unretweet_post(postid):
    """
    used to unretweet a tweet
    @params postid Postid of the post to unretweet
    """
    if False == is_logged_in():
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
    if is_logged_in() == False:
        set_message("Please Login to like tweets", "danger")
        return "login"
    if request.method == 'GET':
        likes = User(session['username']).like_post(postid)
        print(likes)
        # return jsonify(likes=likes)


@app.route('/unlike/<postid>', methods=['GET'])
def unlike_post(postid):
    """
    unlike a users post
    @params postid Postid of the post to unlike
    """
    if is_logged_in() == False:
        set_message("Please Login to like tweets", "danger")
        return redirect('/login', '302')
    if request.method == 'GET':
        User(session['username']).unlike_tweet(postid)
        return 'Like'


@app.route('/usernetwork', methods=['GET'])
def usernetwork():
    """
    used for the tab that enables the visualisation of a D3js visualization of
    application wide user network of users, with follow relationships indicated,
    and each user also labelled by username and total number of likes of tweets
    """
    if is_logged_in() == False:
        return redirect('/login', '302')
    dump_user_network()
    template = env.get_template("user-networkD3.html")
    session_user_json = User(session['username']).get_json_user()
    return template.render(
        session_user=session_user_json,
        user=session_user_json
    )


if __name__ == '__main__':
    app.run(debug=True)
