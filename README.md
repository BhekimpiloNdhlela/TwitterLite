# TwitterLite

## Setup Instructions
To get up and running follow the following steps. If I get time I will probably write a python
script for this. However, for now this is what we have to do to get started with a functional development environment.

#### First time Setup
```bash
$ git clone https://github.com/BhekimpiloNdhlela/405-Found.git
$ cd TwitterLite
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### Setting Up Sendgrid API_KEY:
Assuming you in **TwitterLite/** folder Get your Api Key from creating a Sendgrid account [here]
(https://signup.sendgrid.com/) And then and then replace **'YOUR_API_KEY'** bellow with the newly obtained api key.
```bash
$ echo "export SENDGRID_API_KEY='YOUR_API_KEY'" >> venv/bin/activate
$ echo "export SALT='SERIALIZING SALT'" >> venv/bin/activate
$ echo "export SECRET_KEY='THE SECRET KEY'" >> venv/bin/activate
$ echo "export DB_USERNAME='THE DB USERNAME'" >> venv/bin/activate
$ echo "export DB_PASSWORD='THE DB PASSWORD'" >> venv/bin/activate
$ echo "export DB_HOST_PORT='THE DB HOST PORT'" >> venv/bin/activate

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
Assuming you in the Virtual enviroment **TwitterLite/** folder
```
$ deactivate
```

#### Activating The Virtual Enviroment
```bash
$ cd 405-Found
$ source venv/bin/activate
```

## Style guide
  [PEP style guide.](https://www.python.org/dev/peps/pep-0008/)

## Project Structure
```
.
├── app                      # Folder containing all the application logic
│   ├── static               
│   ├── templates            
│   ├── run.py               
│   └── utils.py             
├── .gitignore
├── README.md
└── requirements.txt
```


## Contributers:

| Names         | Surname      |
| ------------- | ------------ |
| Bhekimpilo    | Ndhlela      |
| David         | Williams     |
| Keanu         | Damon        |
| Klensch       | Lucas        |
| Nishaat       | Laher        |
| Tahir         | Rhoda        |
