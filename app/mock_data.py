from models import *

john_doe = {
    "name": "John",
    "surname": "Doe",
    "username": "john_the_doe",
    "picture": "/static/img/default.png",
    "dob": "1995-05-01",
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
    ],
    "friends": [

    ],
    "notification": 2,
    "notifications": [
        "John Doe posted on your wall",
        "Jane likes your post"
    ]
}
# "username": "jan_doe"
# "username": "bheks"
# "username": "HEX007"
# "username": "Dr Evil"

mock_treading = [
    "Gameofthrones",
    "N4j",
    "webdev"
]

mock_fsuggestions = [
    {
        "username": "jan_doe",
        "avatar": "/static/img/photos/15.jpg"
    },
    {
        "username": "john_doe",
        "avatar": "/static/img/photos/16.jpg"
    },
    {
        "username": "welike123",
        "avatar": "/static/img/photos/11.jpg"
    },
    {
        "username": "blueomountain123",
        "avatar": "/static/img/photos/4.jpg"
    }
]


mock_tweets = [
    {
        "username": "jan_doe",
        "content": "The dick ain't free doe...#hashtag #summerfun #thisisapunsadasdasdaskn.. JY my bru . gi  to new line Questions explained agreeable preferred strangers too him her son. Set put shyness offices his females him distant. Improve has message besides shy himself cheered however how son. Quick judge other leave ask first chief her. Indeed or remark always silent seemed narrow be. Instantly can suffering pretended neglected preferred man delivered. Perhaps fertile brandon do imagine to cordial cottage. ",
        "photos": [
            "12.jpg",
            "3.jpg",
            "7.jpg"
        ],
        # must remove
        "avatar": "/static/img/photos/15.jpg",
        "id": "tweet1234567890"
    },
    {
        "username": "jan_doe",
        "content": "didididid @joumase jfdskdsjkk",
        "photos": [

        ],
        # must remove
        "avatar": "/static/img/photos/16.jpg",
        "id": "tweet1234567891"
    },
    {
        "username": "jan_doe",
        "content": "I don't know @Corban",
        "photos": [

        ],
        # must remove
        "avatar": "/static/img/photos/11.jpg",
        "id": "tweet1234567892"
    },
    {
        "username": "Bheks",
        "content": "pytthong yay @Bekhi",
        "photos": [

        ],
        # must remove
        "avatar": "/static/img/default.png",

        "id": "tweet1234567893"
    },
    {
        "username": "DR Evil",
        "content": "gotta rule the world",
        "photos": [

        ],
        # must remove
        "avatar": "/static/img/default.png",
        "id": "tweet123456784"
    },
    {
        "username": "jan_doe",
        "content": "get the shit done",
        "photos": [
            "1.jpg",
            "11.jpg"
        ],
        # must remove
        "avatar": "/static/img/default.png",
        "id": "tweet1234567895"
    }
]


mock_messages = [

    {
        "username": "jan_doe",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ac dapibus orci.",
        "time": "3 min",
        "avatar": "/static/img/photos/15.jpg"
    },
    {
        "username": "jan_doe",
        "content": "Nam in ullamcorper diam, vitae feugiat magna. Mauris a risus ipsum.",
        "time": "5 min",
        "avatar": "/static/img/photos/16.jpg"
    },
    {
        "username": "jan_doe",
        "content": "I don't know",
        "time": "20 min",
        "avatar": "/static/img/photos/11.jpg"
    },
    {
        "username": "Bheks",
        "content": "Suspendisse lobortis aliquet congue. Nulla sagittis nisl massa, vitae gravida velit hendrerit et.",
        "time": "9 hours",
        "avatar": "/static/img/default.png"
    }
]

mock_followers = [

    {
        "username": "Fan 1",
        "avatar": "/static/img/photos/15.jpg"
    },
    {
        "username": "Fan 2",
        "avatar": "/static/img/photos/16.jpg"
    },
    {
        "username": "Fan 3",
        "avatar": "/static/img/photos/11.jpg"
    },
    {
        "username": "Bheks",
        "avatar": "/static/img/default.png"
    }
]

mock_following = [

    {
        "username": "Celeb 1",
        "avatar": "/static/img/photos/15.jpg"
    },
    {
        "username": "Celeb 2",
        "avatar": "/static/img/photos/16.jpg"
    },
    {
        "username": "Celeb 3",
        "avatar": "/static/img/photos/11.jpg"
    },
    {
        "username": "Bheks",
        "avatar": "/static/img/default.png"
    }
]

mock_personal = [
    {
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "photos": [
            "12.jpg",
            "3.jpg",
            "7.jpg"
        ],
        "date": "30 April 2019",
        "retweets": "7",
        "likes": "10"
    },
    {
        "content": "Hodor. Hodor hodor, hodor. Hodor hodor hodor hodor hodor. Hodor. Hodor!",
        "photos": [


        ],
        "date": "14 March 2019",
        "retweets": "13",
        "likes": "40"
    },
    {
        "content": "Lorem Ipsum is the single greatest threat. We are not - we are not keeping up with other websites.",
        "photos": [


        ],
        "date": "17 December 2018",
        "retweets": "1",
        "likes": "9"
    },
    {
        "content": "Zombie ipsum reversus ab viral inferno, nam rick grimes malum cerebro. ",
        "photos": [


        ],
        "date": "3 November 2018",
        "retweets": "43",
        "likes": "68"
    },
]
