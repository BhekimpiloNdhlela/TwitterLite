# 405-Found

Repository for Web Development RW334 Project 2.

## Members

Bhekimpilo Ndhlela **18998712**  
David Williams **19869355**  
Keanu Damons **19791615**
Klensch Lucas **19908687**  
Nishaat Laher **21183635**
Tahir Rhoda **20175086**

## Setup

To get up and running follow the following steps. If I get time I will probably write a python script
for this. However, for now this is what we have to do to get the development enviroment working.

#### First time Setup

```bash
$ git clone https://github.com/BhekimpiloNdhlela/405-Found.git
$ virtualenv 405-Found
$ cd 405-Found
$ source bin/activate
$ pip install -r requirements.txt
```

#### Running app on Local Server

Make sure you successfully completed the **First Time Setup** steps before rennuning the application.

```bash
$ python app/run.py
```
visit: [http://127.0.0.1:5000/](http://127.0.0.1:5000/) 

#### Deactivating The Virtual Enviroment

Assuming you in the Virtual enviroment **405-Found/** folder
```
$ deactivate
```

#### Activating The Virtual Enviroment

```
$ cd 405-Found
$ source bin/activate
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
