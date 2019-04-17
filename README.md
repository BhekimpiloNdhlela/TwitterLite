# 405-Found

Repository for Web Development RW334 Project 2.

## Members

Bhekimpilo Ndhlela (18998712)  
David Williams (19869355)  
Keanu Damons (19791615)  
Klensch Lucas (19908687)  
Nishaat Laher (21183635)  
Tahir Rhoda (20175086)

## Setup

To get up and running as soon as possible

### First time Setup

Clone the repository to your machine  
Everything will be install inside virtualenv, using pip  
To install on your local/narga machine.

```bash
git clone https://github.com/BhekimpiloNdhlela/405-Found.git
cd 405-Found
pip install -r requirements.txt
python run.py
```

### Running app on Local Server

For first running first check the _first time setup_ above

```bash
python run.py
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
