from utils import get_date, get_password_hash, get_time_stamp, get_password_verification
from py2neo import Graph, Node, Relationship, authenticate
import uuid

"""
THANK YOU KLENSCH FOR CREATING THE CLOUD CONTAINER or VIRTUAL MACHINE :-)

TODO: db credentials(username, password, http_port, https_port, http_port and host_port)
should be made enviroment variables or should be stored in the config file. for good
practice and safety reasons.
"""

user = '405-found'
password = 'b.W3k0rCRmt6Cm.dxDei5UcxeeS6aTP'
host_port = 'hobby-jieinjmgjfpbgbkecpnglccl.dbs.graphenedb.com:24780'
DB_HTTP_PORT, DB_HTTPS_PORT = 24789, 24780

# authenticate before creating the Graph instance
authenticate(host_port, user, password)
# if authenticated create a Graph instance
graph = Graph(
    'https://'+host_port+'/db/data/',
    bolt=False,
    secure=True,
    http_port=DB_HTTP_PORT,
    https_port=DB_HTTPS_PORT
)

DEFAULT_AVATAR = "/static/img/default.png"


class User:
    """ doc-string """

    def __init__(self, user_email):
        """ constructor of the user object or instance """
        self.useremail = useremail

    def is_account_verified(self):
        """ doc-string """
        this = get_this()
        return this['']

    def update_verification_account(self):
        """ doc-string """
        me = get_this()
        me['accountverrified'] = True

    def update_user_bio(self, newbio):
        """ doc-string """
        this = get_this()
        this['bio'] = newbio

    def update_user_avatar(self, new_avatar):
        """ doc-string """
        this = get_this()
        this['useravatar'] = new_avatar

    def update_password_hash(self, newhash):
        """ used to update the users password hash """
        this = get_this()
        this['passwordhash'] = newhash

    def get_this(self):
        """
        used to get me, the user that was created with the constructor of
        this instance.

        Returns -> me: if found else None
        """
        this = graph.find_one('User', 'useremail', self.useremail)
        return this

    def get_password_hash(self):
        """ doc-string """
        this = get_this()
        return this['passwordhash']

    def get_user_name(self):
        """ doc-string """
        this = get_this()
        return this['username']

    def get_user_firstname(self):
        """ docs """
        this = get_this()
        return this['firstname']

    def get_user_lastname(self):
        """ docs """
        this = get_this()
        return this['lastname']

    def get_user_email(self):
        """ doc-string """
        this = get_this()
        return this['useremail']

    def get_user_DOB(self):
        this = get_this()
        return this['dob']

    def get_user_bio(self):
        """ doc-string """
        this = get_this()
        return this['bio']

    def get_user_avatar(self, user_name):
        """ doc-string """
        this = get_this()
        return this['avatar']

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

        this = get_this_user()
        if this['accountverrified']:
            is_correct = get_password_verification(
                this['passwordhash'], password)
            return 0 if is_correct else 1
        else:
            return -1

    def get_location_coorl(self, user_name):
        """ doc-string """
        this = get_this()
        return this['location']

    def update_location_coords(self, latitude, longtitude):
        this = get_this()
        this['location'] = {
            'latitude': latitude,
            'longtitude': longtitude
        }

    def add_user(self, username, firstname, lastname, dob, gender, passwordhash):
        """
        this is a function used only once, that is if the user is creating
        a user profile with the application.

        Returns -> False if the user exists else a new user is created
        """
        # check if user is in the db return if False
        if graph.find_one('User', 'useremail', self.useremail):
            return False
        # else add the user to the db
        usernode = Node(
            'User',
            username=username,
            firstname=firstname,
            lastname=lastname,
            bio='',
            dob=dob,
            gender=gender,
            passwordhash=passwordhash,
            createdat=get_time_stamp(),
            useavatar=DEFAULT_AVATAR,
            accountverrified=False,
            location={
                'latitude': None,
                'latitude': None
            },
            posts=[],
            friends=[],
            firendrequest=[],
            notifications=[]
        )
        graph.create(usernode)
        return True

    def get_user_friends(self):
        """ doc-string """
        pass

    def get_user_posts(self):
        """ doc-string """
        pass

    def add_post(self):
        pass

    def __str__(self):
        """ doc-string """
        return None

    def overwrite_email_verification():
        """ Must Overwrite the verification process """
        return null

    def get_json_user(self):
        user = get_this()
        """ Json data """
        return {
            "name": user['firstname'],
            "surname": user['lastname'],
            "username": user['username'],
            "picture": user['avatar'],
            "dob": user['dob'],
            "title": "Web dev Specialist",
            "location": "Your mom's house",
            "photos": [
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


"""----------------------------------------------------------------------------"""


class Post:
    """
    doc-string
    """

    def __init__(self, *args, **kwargs):
        """
        doc-string
        """
        pass

    def getPost(self):
        """
        doc-string
        """
        pass

    def getPostOwner(self):
        """
        doc-string
        """
        pass

    def getPostDatetime(self):
        """ doc-string """
        pass

    def getPostLikes(self):
        """ doc-string """
        pass

    def getPostComments(self):
        """ doc-string """
        pass

    def getPostTitle(self):
        """ doc-string """
        pass

    def getPostUUID(self):
        """ doc string """
        pass

    def updatePost(self):
        """ doc-string """
        pass

    def updatePostTitle(self):
        """ doc-string """
        pass

    def getPostTags(self):
        """ doc-string """
        pass

    def updatePostTags(self):
        """ doc-string """
        pass

    def __str__(self):
        """ doc-string """
        pass
