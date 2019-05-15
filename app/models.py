import uuid
from py2neo import authenticate, Graph, Node, Relationship
from utils import get_time_stamp, get_password_hash, get_time_stamp, get_password_verification
import os
import json

DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST_PORT = os.environ.get('DB_HOST_PORT')
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

        Returns -> -1 : Account does no exist
                    0 : signin success
                    1 : Wrong Password
                   -2 : Account not verrified
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
        # check if user is in the db return False if found
        if graph.find_one('User', 'username', self.username): return False
        # else add the user to the db and return True
        usernode = Node(
            'User',
            username=self.username,
            useremail=email,
            firstname=firstname,
            lastname=lastname,
            gender=gender,
            passwordhash=passwordhash,
            dob=dob,
            useravatar=DEFAULT_AVATAR,
            accountverrified=False,
            bio='Hi I just started using Bootleg Twitter!',
            title='Title not set.',
            createdate=get_time_stamp(),
            notifications=[
                'welcome to bootleg twitter, enjoy.',
                'edit your details',
                'enjoy the stay'
            ],
            notification=2
        )
        graph.create(usernode)
        return True


    def get_json_user(self):
        """ Json data """
        user = self.get_this_user_data()
        return {
            "name": user['firstname'],
            "surname": user['lastname'],
            "username": user['username'],
            "picture": user['useravatar'],
            "dob": user['dob'],
            "title": user['title'],
            "avatar": user['useravatar'],
            "bio": user['bio'],
            "gender": user['gender'],
            "notification": user['notification'],
            "notifications": user['notifications'],
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


    def get_this_user_data(self):
        """
        used to get me, the user that was created with the constructor of
        this instance.

        Returns -> this: if found else None
        """
        return graph.find_one('User', 'username', self.username)


    def verify_user_account(self):
        """
        used to update the users account verification status
        """
        this = self.get_this_user_data()
        graph.merge(this)
        this['accountverrified'] = True
        this.push()


    def update_user_details(self, firstname, lastname, dob, title, bio):
        """
        used to update the users details: firstname, lastname, bio, title, dob
        """
        this = self.get_this_user_data()
        graph.merge(this)
        this['firstname'] = firstname
        this['lastname']  = lastname
        this['newdob']    = dob
        this['title']     = title
        this['bio']       = bio
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
        gets the user date of birth of the user that this object's instance
        was created for
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


    def get_json_post(self, postid):
        """
        used to return a posts details in jason format, this is unnecessary but
        Klensch insisted i do this.
        """
        post = graph.find_one('Post', 'id', postid)
        return {
            'id'        : post['id'],
            'tweet'     : post['tweet'],
            'timestamp' : post['timestamp'],
            'date'      : post['date'],
            'retweets'  : post['retweets'],
            'likes'     : post['likes'],
            'photos'    : post['photos']
        }


    def add_post(self, tweet, hashtags, taggedusers):
        """
        add post to the graph and create a published relationship between the
        user and the post as well as the post and its tags
        """
        user = self.get_this_user_data()
        post = Node(
                    'Post',
                    id=str(uuid.uuid4()),
                    tweet=tweet,
                    date=get_time_stamp(),
                    hashtags=hashtags,
                    taggedusers=taggedusers,
                    retweets=0,
                    likes=0,
                    comments=0,
                    photos=[]
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


    def get_user_followers(self):
        """
        used to get the users that are following this user
        """
        query = '''
        MATCH (user:User)-[:FOLLOWING]->(follower:User)
        WHERE follower.username = {username}
        RETURN user
        '''
        queryresults = graph.run(query, username=self.username)
        return set([result['user'] for result in queryresults])


    def get_user_following(self):
        """
        used to get the user names that this user is following
        """
        query = '''
        MATCH (user:User)-[:FOLLOWING]->(following:User)
        WHERE user.username = {username}
        RETURN following
        '''
        queryresults = graph.run(query, username=self.username)
        return set([result['following'] for result in queryresults])


    def get_user_posts(self):
        """
        used to get all the post id a user has posted
        """
        query = '''
        MATCH (user:User)-[:PUBLISHED]->(post:Post)
        WHERE user.username = {username}
        RETURN post
        '''
        queryresults = graph.run(query, username=self.username)
        return [result['post'] for result in queryresults]


    def get_recent_posts(self):
        """
        return the most recent posts id of a users followers functionailty-10
        """
        query = '''
        MATCH (:User {username: {username}})-[:PUBLISHED]->(post:Post)
        RETURN post
        ORDER BY post.date DESC LIMIT 6
        '''
        queryresults = graph.run(query, username=self.username)
        return [result['post']['id'] for result in queryresults]


    def get_timeline_posts(self, interation=0):
        """
        return the most recent Tweets for the user for their timeline
        @params self Intstance of itself
        @params interation Skips over this number of post for dynamic loading
        @return posts An Array of the posts
        """
        query = '''
        MATCH (:User {username: {username}})-[:FOLLOWING]->(u:User)-[:PUBLISHED]->(p:Post) 
        WITH collect({user: u, post: p}) AS R1

        MATCH (user:User {username: {username}})-[:PUBLISHED]->(post:Post)
        WITH R1 + collect({user: user, post: post}) AS R2

        MATCH (user)-[:RETWEETED]->(rpost:Post)
        WITH R2 + collect({user: user, post: rpost}) AS R3

        MATCH (user)-[:FOLLOWING]->(rruser:User)-[:RETWEETED]->(rrpost:Post)
        WITH R3 + collect({user: rruser, post: rrpost}) AS R4

        UNWIND R4 AS row
        RETURN row.user AS users, row.post AS posts
        ORDER BY posts.date DESC
        LIMIT 50
        '''
        queryresults = graph.run(
            query,
            username=self.username
        )
        return [[results['users'], results['posts']] for results in queryresults]


    def get_recommended_users(self):
        """
        return recommend users for the logged in user
        @params self Intstance of itself
        @return posts An Array of the users
        """
        query = '''
        MATCH (users:User)
        WHERE NOT (:User {username: {username}})-[*1..3]->(users:User)
        AND NOT users.username = {username}
        RETURN users
        LIMIT 5
        '''
        queryresults = graph.run(query, username=self.username)
        return [results['users'] for results in queryresults]


    def retweet_post(self, postid):
        """
        used to retweet a tweet or post with the aid of an postid
        """
        query = '''
        MATCH (user:User),(post:Post)
        WHERE user.username = {username} AND post.id = {postid}
        SET post.retweets = post.retweets + 1
        CREATE (user)-[r:RETWEETED]->(post)
        RETURN r
        '''
        graph.run(query, username=self.username, postid=postid)


    def like_post(self, postid):
        """
        used to like a post, also increments the like field by one.
        """
        query = '''
        MATCH (user:User),(post:Post)
        WHERE user.username = {username} AND post.id = {postid}
        SET post.likes = toInteger(post.likes + 1)
        CREATE (user)-[r:LIKES]->(post)
        RETURN post.likes
        '''
        return set(graph.run(query, username=self.username, postid=postid))


    def follow_user(self, username):
        """
        used to follow a user
        @param username the username of the user to follow
        """
        if self.is_following(username) == False:
            query = '''
            MATCH (user:User),(following:User)
            WHERE user.username = {username} AND following.username = {fusername}
            CREATE (user)-[r:FOLLOWING]->(following)
            RETURN r
            '''
            graph.run(query, username=self.username, fusername=username)


    def unfollow_user(self, username):
        """
        delete a FOLLOWING relationation that exist between a this and the other
        user given a username of the user to unfollow.
        """
        query = '''
        MATCH (user:User)-[r:FOLLOWING]->(following:User)
        WHERE user.username = {myusername} AND following.username = {username}
        DELETE r
        '''
        graph.run(query, myusername=self.username, username=username)


    def unlike_tweet(self, postid):
        """
        delete a LIKES relationation that exist between a user and a post
        given a post id
        """
        query = '''
        MATCH (user:User)-[r:LIKES]->(post:Post)
        WHERE user.username = {username} AND post.id = {postid}
        SET post.likes = post.likes - 1
        DELETE r
        '''
        graph.run(query, username=self.username, postid=postid)


    def unretweet_tweet(self, postid):
        """
        delete a RETWEET relationation that exist between a user and a post
        given a post id
        """
        query = '''
        MATCH (user:User)-[r:RETWEETED]->(post:Post)
        WHERE user.username = {username} AND post.id = {postid}
        SET post.retweets = post.retweets - 1
        DELETE r
        '''
        graph.run(query, username=self.username, postid=postid)


    def is_following(self, username):
        """
        check if this user is following the other user
        """
        query = '''
        MATCH (user:User)-[:FOLLOWING]->(following:User)
        WHERE user.username = {username} AND following.username = {fusername}
        RETURN following.username
        '''
        queryresults = graph.run(
            query,
            username=self.username,
            fusername=username
        )
        return username in [res['following.username'] for res in queryresults]


    def check_post_like(self, postid):
        """
        check if there is a user post LIKE relationship
        """
        pass


    def check_post_retweet(self, postid):
        """
        check if there is a user post RETWEET relationship
        """
        pass


    def get_user_suggestions(self):
        """
        doc-string
        """
        pass


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Graph Database functions that are not related to creating a user instance
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_tweet_likes_usernames(postid):
    """
    get all the usernames of users that liked a tweet, make use of the tweetid
    or postid to search for the usernames that liked a post or tweet
    """
    query = '''
    MATCH (post:Post)-[:LIKES]-(user:User)
    WHERE post.id = {postid}
    RETURN user.username
    '''
    queryresults = graph.run(query, postid=postid)
    return set([result['user.username'] for result in queryresults])


def get_tweet_retweets_usernames(postid):
    """
    get all the usernames of users that retweeded a tweet, make use of the
    tweetid or postid to search for the usernames that retweeted a post or
    tweet
    """
    query = '''
    MATCH (post:Post)-[:RETWEETED]-(user:User)
    WHERE post.id = {postid}
    RETURN user.username
    '''
    queryresults = graph.run(query, postid=postid)
    return set([result['user.username'] for result in queryresults])


def get_tweets_by_hashtag(user, hashtag):
    """
    Be able to select a particular hashtag, and see tweets with this hashtag
    (ordered by time)
    returns all the posts correspoinding to the given hashtag.
    """
    #limit can be removed, take out the following if its not needed for 8a.
    query = '''
    MATCH (:User {username: {user}})-[:FOLLOWING]->(users:User)-[:PUBLISHED]->(posts:Post)<-[:HASHTAG]-(tags:Tag {name: {hashtag}})
    RETURN tags, posts, users
    ORDER BY posts.timestamp DESC
    LIMIT 20 
    '''
    queryresults = graph.run(query, user=user, hashtag=hashtag)
    return [[results['users'], results['posts']] for results in queryresults]


def get_trending_hashtags_for_user(user):
    """
    This gets the top 5 hashtags ordered by likes and occurences
    """
    query = '''
    MATCH (:User {username: {user}})-[:FOLLOWING]->(:User)-[:PUBLISHED]->(posts:Post)<-[:HASHTAG]-(tags:Tag)
    RETURN tags.name, count(tags) as t, sum(posts.likes) as p
    ORDER BY p DESC, t DESC
    LIMIT 5
    '''
    queryresults = graph.run(query, user=user)
    return [results['tags.name'] for results in queryresults]

    
def search_users(string):
    """
    return recommend users for the logged in user
    @params self Intstance of itself
    @return posts An Array of the users
    """
    query = '''
    MATCH(users: User)
    WHERE users.username CONTAINS {string}
    RETURN users.username AS username
    LIMIT 5
    '''
    return [results['username'] for results in graph.run(query, string=string)]


def dump_user_network():
    """
    used for the tab that enables the visualisation of a D3js visualization of
    application wide user network of users, with follow relationships indicated,
    and each user also labelled by username and total number of likes of tweets
    """
    # get all the usernames from the database, this is neccessary because i
    # dont want to skip users that dont have posts of that are not being followed
    # or following any one. Hence this query gets all the users regardless of their
    # status in the application.

    D3dict, data = {}, {}
    data['nodes'], data['links'] = [], []

    query = '''
    MATCH (a:User)
    RETURN a.username AS username
    '''

    for key in graph.run(query):
        D3dict[key['username']] = 0

    query = '''
    MATCH (u:User)-[:PUBLISHED]->(p:Post)
    RETURN u.username AS username, SUM(p.likes) AS totallikes
    '''

    for likedata in graph.run(query):
        D3dict[likedata['username']] = likedata['totallikes']
    for key in D3dict:
        data['nodes'].append(
            {
                "username": key,
                "postlikes": D3dict[key]
            }
        )
    for key in D3dict:
        following = __get_following_usernames(key)
        for user in following:
            data['links'].append(
                {
                    "source": key,
                    "target": user,
                    "type": "FOLLOWING"
                }
            )
    with open("static/miserables.json", 'w') as f:
        json_data = json.dump(data, f)

def __get_following_usernames(username):
    """
    helper function used to get the user names that a specific user is following
    this function is a helper function of obtaining the D3js visualisation
    functionality
    """
    query = '''
    MATCH (user:User)-[FOLLOWING]->(following:User)
    WHERE user.username = {username}
    RETURN following.username AS username
    '''
    return set(user['username'] for user in graph.run(query, username=username))


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Test client for models. [NOTE used during development stage]
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':
    dump_user_network()
    User('keanudamon123').retweet_post('27f017b8-32a0-4b0b-a301-dcc3bba8c57f')
    User('nish').retweet_post('27f017b8-32a0-4b0b-a301-dcc3bba8c57f')
    User('keanud').retweet_post('27f017b8-32a0-4b0b-a301-dcc3bba8c57f')
    print("Retweeting")
    # test retweeting, make Corban retweet the post
    User('Corban').retweet_post('e48c3d0a-66f7-48ea-a069-d98ca6e02216')
    User('keanud').retweet_post('2a73d1c0-4546-46e1-adcd-dd37d91da15f')
    User('Corban').retweet_post('250f2a79-59ee-4700-aa1e-b2c7594cedb2')
    User('keanudamon123').retweet_post('250f2a79-59ee-4700-aa1e-b2c7594cedb2')
    User('nish').retweet_post('250f2a79-59ee-4700-aa1e-b2c7594cedb2')
    User('keanud').retweet_post('250f2a79-59ee-4700-aa1e-b2c7594cedb2')
    User('nish').like_post('250f2a79-59ee-4700-aa1e-b2c7594cedb2')
    User('Corban').like_post('250f2a79-59ee-4700-aa1e-b2c7594cedb2')
    User('keanudamon123').like_post('250f2a79-59ee-4700-aa1e-b2c7594cedb2')
    User('Corban').retweet_post('e48c3d0a-66f7-48ea-a069-d98ca6e02216')
    print("done retweeting")

    # check if i am following nish and tahir
    print(User('HexDEADBEEF').is_following('nish'), "True following Nish")
    print(User('HexDEADBEEF').is_following('tahir'), "False not following Tahir")

    User('HexDEADBEEF').follow_user('Corban')
    user_following_users = User('HexDEADBEEF').get_user_following()
    print("\n\nUSERS THAT I AM FOLLOWING")
    [print(following) for following in user_following_users]

    # unfollow Corban
    User('HexDEADBEEF').unfollow_user('Corban')
    print("\n\nUSERS THAT I AM FOLLOWING")
    user_following_users = User('HexDEADBEEF').get_user_following()
    print("following")
    [print(following['username']) for following in user_following_users]
    print(User('HexDEADBEEF').is_following('nish'), "am i following nish")
    print(User('HexDEADBEEF').is_following('tahir'), 'am i following tahir')
    # get all the posts that HexDEADBEEF has posted

    print("\ALL MY POSTS ID")
    user_recent_posts = User('HexDEADBEEF').get_user_posts()
    [print(post['hashtags']) for post in user_recent_posts]

    # get the users that are following HexDEADBEEF
    print("\n\nUSERS THAT I AM FOLLOWING")
    user_following_users = User('HexDEADBEEF').get_user_following()
    [print(following) for following in user_following_users]

    # get users that are following nish
    user_followers = User('nish').get_user_followers()
    for u in user_followers:
        print(u['username'])

    print("\n\nNISH's FOLLOWERS")
    [print(follower) for follower in user_followers]
    print('\n\nMY RECENT POSTS')
    users_recent_posts = User('HexDEADBEEF').get_recent_posts()
    [print(recentpost) for recentpost in users_recent_posts]

    # make keanu follow me
    user = User('Corban').follow_user('HexDEADBEEF')
    user = User('klensch_the_machine').follow_user('HexDEADBEEF')
    user = User('keanudamon123').follow_user('HexDEADBEEF')
    user = User('nish').follow_user('HexDEADBEEF')
    user = User('klensch_the_machine').follow_user('nish')
    user = User('nish').follow_user('klensch_the_machine')
    user = User('klensch_the_machine').follow_user('Corban')
    user = User('keanudamon123').follow_user('klensch_the_machine')

    # get the usernames of people that like the post with post id:
    # '250f2a79-59ee-4700-aa1e-b2c7594cedb2'
    print("\n\nPOST LIKERS")
    postlikers = get_tweet_likes_usernames('250f2a79-59ee-4700-aa1e-b2c7594cedb2')
    [print(postliker) for postliker in postlikers]

    # get the usernames of people that retweeted a post with postid:
    # '250f2a79-59ee-4700-aa1e-b2c7594cedb2'
    print("\n\nPOST RETWEETERS")
    postretweeters = get_tweet_retweets_usernames('250f2a79-59ee-4700-aa1e-b2c7594cedb2')
    [print(postretweeter) for postretweeter in postretweeters]
    """
    #KLENSCH!!! THIS AINT WORKING LAD!!!
    query = '''
    MATCH (u:User)-[:PUBLISHED]->(p:Post)
    RETURN u.username AS username, SUM(p.likes) AS totallikes
    UNION
    MATCH (a:User)
    RETURN a.username AS username, 0 AS totallikes
    '''
    # initialise the D3 data that should be converted to JSON format
    D3dict = dict((key['username'], [set(), key['totallikes']]) for key in graph.run(query))

    for i in D3dict:
        print(D3dict[i])
    """
