class User:
    """
    doc-string
    """
    def __init__(self, user_name, user_email, user_dob, user_hash, user_gender, user_bio=None, user_avatar=None):
        """
        doc-string
        """
        self.user_name = user_name
        self.user_email = user_email
        self.user_dob = user_dob
        self.user_hash = user_hash
        self.user_gender = user_gender
        self.user_bio = user_bio
        self.user_avatar = user_avatar

    def getPasswordHash(self):
        """
        doc-string
        """
        return self.user_hash

    def getUserName(self):
        """
        doc-string
        """
        return self.user_name

    def getUserEmail(self):
        """
        doc-string
        """
        return self.user_email

    def getUserBOB(self):
        """
        doc-string
        """
        return self.user_dob

    def getUserBio(self):
        """
        doc-string
        """
        return self.user_bio

    def getUserAvatar(self):
        """
        doc-string
        """
        return self.user_avatar

    def updateUserhash(self, new_hash):
        """
        doc-string
        """
        self.user_hash = new_hash

    def updateUserBio(self, new_bio):
        """
        doc-string
        """
        self.user_bio = new_bio

    def updateUserAvatar(self, new_avatar):
        """
        doc-string
        """
        self.user_avatar = new_avatar

    def addPost(self):
        pass

    def __eq__(self, this, other):
        """
        doc-string
        """
        return None

    def getUserFriends(self):
        """
        doc-string
        """
        pass

    def __str__(self):
        """
        doc-string
        """
        return None

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
        """
        doc-string
        """
        pass

    def getPostLikes(self):
        """
        doc-string
        """
        pass

    def getPostComments(self):
        """
        doc-string
        """
        pass

    def getPostTitle(self):
        """
        doc-string
        """
        pass

    def getPostUUID(self):
        """
        doc-string
        """
        pass

    def updatePost(self):
        """
        doc-string
        """
        pass

    def updatePostTitle(self):
        """
        doc-string
        """
        pass

    def getPostTags(self):
        """
        doc-string
        """
        pass

    def updatePostTags(self):
        """
        doc-string
        """
        pass

    def __str__(self):
        """
        doc-string
        """
        pass

