# 405-Found

Repository for Web Development RW334 Project 2.

## Members

Bhekimpilo Ndhlela **18998712**

David Williams **19869355**

Keanu Damons **19791615**

Klensch Lucas **19908687**

Nishaat Laher **21183635**

Tahir Rhoda **20175086**

## TODOS:
- [ ] Make the **run.py** script specific for handling the running of the application. Move  
nessary code (views) in the run.py script to **views.py** and also move the necessary code in the 
**views.py** to **utils.py**

- [ ] create a config.cnfg (i think, I am not sure about the extension or if it matters) for storing API_KEYs and hashes accossiated to the application.
- [x] Create Project Repository for Version	control.
- [x] Create Trello board for issue management or Project	Management [follw this link to the Trello board](https://trello.com/b/EU293DyA/bootleg-twitter)

- [x] Create Signin Form ***Frontend***
- [x] Create Signup form ***Frontend***
- [x] Create Forgot-Password Form ***Frontend*** Still needs to be changed.
- [ ] Registration page for first time users.
- [ ] Login with username and	password.
- [ ] Validate the password strength with an appropriate	regular	expression.
- [ ] Profile	page where you can add your photo, write a short bio about yourself that people
following	you, or who would like to follow you, can see, and where you can change	your password.
- [ ] Be able to suggest people to follow. This must be a list of people followed	by those you are
following and that	you	are	not	already	following, ordered based on total number of likes they have 
received on tweets, and secondly on total number of tweets.
- [ ] Be able to tweet, retweet and like a tweet. Also, be able to add a hashtag to a tweet.
- [ ] Tabs that can be selected to see all your tweets, with number of retweets (by username of
person that did the retweet) and likes indicated, ordered from most recent to oldest, a list of people
you	are	following, and a list of people who are following you.
- [ ] Be able to select a particular hashtag, and see tweets with this hashtag (ordered by time), selected from
a	list of 5 most popular hashtags, based on likes and secondly total number of tweets with this hashtag,
from users you are following.
- [ ] A	hashtag	automatically	becomes	a	clickable	link when you tweet it. Anyone who sees the hashtag can click on 
it and be brought to a page featuring the feed of all the	most recent tweets that contain that particular hashtag.
- [ ] Be able to view tweets of people you are following, ordered by time of tweet and likes that a tweet received.
- [ ] Add a tab that can be used to see a	**D3.js** visualization	of the network of users, with follow relationships
indicated, and each user also labelled by username and total number of likes of tweets. [See	for	example](https://medium.com/statuscode/rethinking-twitters-who-to-follow-using-node-jsand-d3-js-d8875d112bc8)
- [ ] For	extra	credit,	use [NLTK](https://www.nltk.org/) for **natural language analysis/processing** on tweets – [see for	example](https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim4ef03213cd21)



## Setup Instructions
To get up and running follow the following steps. If I get time I will probably write a python
script for this. However, for now this is what we have to do to get the development enviroment working.

#### First time Setup
```bash
$ git clone https://github.com/BhekimpiloNdhlela/405-Found.git
$ cd 405-Found
$ virtualenv -p python3 venv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### Setting Up Sendgrid API_KEY:
Assuming you in the Virtual enviroment **405-Found/** folder
Get your Api Key from creating a Sendgrid account [here](https://signup.sendgrid.com/)
And then copy your API KEY in to the following **'YOUR_API_KEY'**
```bash
# make sure you append while pipping, hence the: >>
$ echo "export SENDGRID_API_KEY='YOUR_API_KEY'" >> venv/bin/activate
$ source venv/bin/activate
```

#### Running The Application on Local Server
Make sure you successfully completed the **First Time Setup**  and **Setting Up Sendgrid API_KEY**
steps before rennuning the application.
```
$ python3 app/run.py
```
visit: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)


#### Deactivating The Virtual Enviroment
Assuming you in the Virtual enviroment **405-Found/** folder
```
$ deactivate
```

#### Activating The Virtual Enviroment
```bash
$ cd 405-Found
$ source venv/bin/activate
```

## Style guide

**Camel case** will be use for _variable_ names and _functions_ names.  
_Filenames_ and _url links_ will be using **dashes** to separate the words.





## Project Structure

```
.
├── app                      # Folder containing all the application logic
│   ├── static               #
│   ├── templates            #
│   ├── run.py               #
│   └── utils.py             #
├── .gitignore
├── README.md
└── requirements.txt         # pip requirements
```
