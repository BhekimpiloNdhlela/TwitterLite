# 405-Found

Repository for Web Development RW334 Project 2.

## Members

| Student Numbers  | Names      | Surname  |
| ---------------- | ---------- | -------- |
| **18998712**     | Bhekimpilo | Ndhlela  |
| **19869355**     | David      | Williams |
| **19791615**     | Keanu      | Damon    |
| **19908687**     | Klensch    | Lucas    |
| **21183635**     | Nishaat    | Laher    |
| **20175086**     | Tahir      | Rhoda    |

## TODOS:
[follow this link to view the todos](https://trello.com/b/EU293DyA/bootleg-twitter)


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
```bash
$ cd app/
$ python3 run.py
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
