from py2neo import Graph, Node, Relationship
from utils import get_date, get_password_hash, get_time_stamp, get_password_verification
import uuid

# global variables
graph = Graph('http://localhost:7474' + '/db/data/', username='neo4j', password='helloworld')
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
            is_correct = get_password_verification(this['passwordhash'], password)
            return 0 if is_correct else 1
        else:
            return -1


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
            lastname=lastname
            dob=dob,
            gender=gender,
            passwordhash=passwordhash,
            createdat=get_time_stamp(),
            useavatar=DEFAULT_AVATAR,
            bio=''
            accountverrified=False,
            location=(),
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
