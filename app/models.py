import uuid
from py2neo import authenticate, Graph, Node, Relationship
from utils import get_time_stamp, get_timestamp_seconds, get_password_hash, get_time_stamp, get_password_verification

"""
TODO: db credentials(username, password, http_port, https_port, http_port and host_port)
should be made enviroment variables or should be stored in the config file. for good
practice and safety reasons.
"""

DB_USERNAME = '405-found'
DB_PASSWORD = 'b.W3k0rCRmt6Cm.dxDei5UcxeeS6aTP'
DB_HOST_PORT = 'hobby-jieinjmgjfpbgbkecpnglccl.dbs.graphenedb.com:24780'
DB_HTTP_PORT, DB_HTTPS_PORT = 24789, 24780

# authenticate before creating the Graph instance
authenticate(DB_HOST_PORT, DB_USERNAME, DB_PASSWORD)
# if authenticated create a Graph instance
graph = Graph(
    'https://'+DB_HOST_PORT+'/db/data/',
    bolt=False,
    secure=True,
    http_port=DB_HTTP_PORT,
    https_port=DB_HTTPS_PORT
)
DEFAULT_AVATAR = "/static/img/default.png"


class User:
    """ doc-string """
    def __init__(self, username):
        """
        constructor of the user object or instance, used to create an instance
        of a user object and then operations can hence be made on that instance
        of the user created by the client.
        """
        self.username = username


    def user_login(self, password):
        """
        used to login the user, this function is called with the password that
        the user enters to the form.
        NOTE: the password is supposed to be check for strength using regular
        expression in validate_password() in utils.py

        Returns ->  -1 : Account Not verified
                    0  : signin success
                    1  : Wrong Password
        """

        this = self.get_this_user_data()
        if not this:
            return -1
        if this['accountverrified']:
            return get_password_verification(this['passwordhash'], password)
        return -2


    def add_user(self, firstname, lastname, email, dob, gender, passwordhash):
        """
        this is a function used only once, that is if the user is creating
        a user profile with the application.

        Returns -> False if the user exists else a new user is created
        """
        # check if user is in the db return if False
        if graph.find_one('User', 'username', self.username):
            return False
        # else add the user to the db
        usernode = Node(
            'User',
            username         = self.username,
            useremail        = email,
            firstname        = firstname,
            lastname         = lastname,
            gender           = gender,
            passwordhash     = passwordhash,
            dob              = dob,
            useravatar       = DEFAULT_AVATAR,
            accountverrified = False,
            bio              = 'Hi I just started using Bootleg Twitter!',
            title            = 'Title not set.',
            createdate       = get_time_stamp(),
            friends          = [],
            notifications    = [
                'welcome to bootleg twitter, enjoy.',
                'edit your details',
                'enjoy the stay'
            ],
            notification     = 2
        )
        graph.create(usernode)
        return True


    def get_json_user(self):
        """ Json data """
        user = self.get_this_user_data()
        return {
            "name"          : user['firstname'],
            "surname"       : user['lastname'],
            "username"      : user['username'],
            "picture"       : user['useravatar'],
            "dob"           : user['dob'],
            "title"         : user['title'],
            "avatar"        : user['useravatar'],
            "bio"           : user['bio'],
            "gender"        : user['gender'],
            "notification"  : user['notification'],
            "notifications" : user['notifications'],
            "location"      : "Your mom's house",
            "photos"        : [
                    "1.jpg",
                    "2.jpg",
                    "3.jpg",
                    "4.jpg",
                    "5.jpg",
                    "6.jpg",
                    "8.jpg",
                    "9.jpg"
            ]
        }


    def get_this_user_data(self):
        """
        used to get me, the user that was created with the constructor of
        this instance.

        Returns -> this: if found else None
        """
        return graph.find_one('User', 'username', self.username)


    def update_user_title(self, newtitle):
        """
        used to update the users title
        """
        this = self.get_this_user_data()
        graph.merge(this)
        this['title'] = newtitle
        this.push()


    def verify_user_account(self):
        """
        used to update the users account verification status
        """
        this = self.get_this_user_data()
        graph.merge(this)
        this['accountverrified'] = True
        this.push()


    def update_user_dob(self, newdob):
        """
        used to update the users date of birth
        """
        this = self.get_this_user_data()
        graph.merge(this)
        this['dob'] = newdob
        this.push()


    def update_user_firstname(self, newfirstname):
        """
        used to update the users first name
        """
        this = self.get_this_user_data()
        graph.merge(this)
        this['firstname'] = newfirstname
        this.push()


    def update_user_lastname(self, newlastname):
        """
        used to update the users last name
        """
        this = self.get_this_user_data()
        graph.merge(this)
        this['lastname'] = newlastname
        this.push()


    def update_user_bio(self, newbio):
        """
        used to update the users bio
        """
        this = self.get_this_user_data()
        graph.merge(this)
        this['bio'] = newbio
        this.push()


    def update_user_avatar(self, newavatar):
        """
        used to update the users avatar or prifile picture
        """
        this = self.get_this_user_data()
        graph.merge(this)
        this['useravatar'] = newavatar
        this.push()


    def update_password_hash(self, newhash):
        """
        used to update the users password hash
        """
        this = self.get_this_user_data()
        graph.merge(this)
        this['passwordhash'] = newhash
        this.push()



    def get_account_veriffication_status(self):
        """
        used to obtain a users account status False if not verified and the
        oposite holds true
        """
        this = self.get_this_user_data()
        return this['accountverrified']


    def get_password_hash(self):
        """
        used to obtain a users password hash, this is for password verification
        reasons.
        """
        this = self.get_this_user_data()
        return this['passwordhash']


    def get_user_name(self):
        """
        gets the user name of the user that this object's instance was created
        for
        """
        this = self.get_this_user_data()
        return this['username']


    def get_user_firstname(self):
        """
        gets the user first name of the user that this object's instance
        was created for
        """
        this = self.get_this_user_data()
        return this['firstname']


    def get_user_lastname(self):
        """
        gets the user last name of the user that this object's instance was
        created for
        """
        this = self.get_this_user_data()
        return this['lastname']


    def get_user_email(self):
        """
        gets the user email of the user that this object's instance was
        created for
        """
        this = self.get_this_user_data()
        return this['useremail']


    def get_user_DOB(self):
        """
        gets the user date of birth of the user that this object's
        instance was created for
        """
        this = self.get_this_user_data()
        return this['dob']


    def get_user_bio(self):
        """
        gets the user biography or status of the user that this object's
        instance was created for
        """
        this = self.get_this_user_data()
        return this['bio']


    def get_user_avatar(self):
        """
        gets the user avatar/ profile picture  of the user that this object's
        instance was created for
        """
        this = self.get_this_user_data()
        return this['avatar']


    def get_location_coordinates(self, user_name):
        """
        doc-string
        """
        this = self.get_this_user_data()
        return this['location']


    def update_location_coords(self, latitude, longtitude):
        this = self.get_this_user_data()
        this['location'] = {
            'latitude': latitude,
            'longtitude': longtitude
        }


    def get_recent_posts(self):
        """
        return the most recent posts of a users followers functionailty-10
        """
        pass


    def get_user_friends(self):
        """
        doc-string
        """
        pass


    def get_user_suggestions(self):
        """
        doc-string
        """
        pass


    def get_hashtag(self):
        """
        return a particular hashtag and show tweets with this hashtag(ordered
        by time) functionality-8
        """
        pass


    def get_user_posts(self):
        """
        return all posts , with the number of likes and retweets and usernames
        of user's who liked and retweeted the post"""
        pass


    def get_user_followers(self):
        """
        return a list of usernames of a user's followers
        """
        pass


    def get_user_followings(self):
        """
        return a list of usernames of a user's followings
        """
        pass

    def add_post(self, tweet, hashtags, taggedusers):
        """
        add post to the graph and create a published relationship between the
        user and the post as well as the post and its tags
        """
        user = self.get_this_user_data()
        post = Node(
                    'Post',
                    id          = str(uuid.uuid4()),
                    tweet       = tweet,
                    timestamp   = get_timestamp_seconds(),
                    date        = get_time_stamp(),
                    likes       = 0,
                    comments    = 0,
                    hashtags    = hashtags,
                    taggedusers = taggedusers
        )

        rel = Relationship(user, 'PUBLISHED', post)
        graph.create(rel)

        # build TAG relationship
        for hashtag in hashtags:
            tag = Node('Tag', name=hashtag)
            graph.merge(tag)
            graph.create(Relationship(tag, 'HASHTAG', post))

        # build TAGGED user relationship
        for taggeduser in taggedusers:
            taggeduser = User(taggeduser).get_this_user_data()
            if taggeduser:
                graph.merge(taggeduser)
                graph.create(Relationship(post, 'TAGGED', taggeduser))
            # else we ignore t`he non existing tagged user

    def like_post(self, post_id):
        """
        doc-string
        """
        user = self.get_this_user_data()
        post = graph.find_one('Post','id', post_id)
        graph.merge(Relationship(user,'likes', post))
