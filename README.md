# TwitterLite

## Setup Instructions
To get up and running follow the following steps. If I get time I will probably write a python
script for this. However, for now this is what we have to do to get started with a functional development environment.

#### First time Setup
```bash
git clone https://github.com/BhekimpiloNdhlela/TwitterLite.git
cd TwitterLite
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### First Time Setup
Assuming you in **TwitterLite/** folder Get your Api Key from creating a Sendgrid account [here]
(https://signup.sendgrid.com/) And then and then replace **'YOUR_API_KEY'** bellow with the newly obtained api key. Also
make sure to set up the correct values for **'SERIALIZING SALT'**, **'THE SECRET KEY'**, **'THE DB USERNAME'**, 
**'THE DB PASSWORD'** and **'THE DB HOST PORT'**
```bash
echo "export SENDGRID_API_KEY='YOUR_API_KEY'" >> venv/bin/activate
echo "export SALT='SERIALIZING SALT'" >> venv/bin/activate
echo "export SECRET_KEY='THE SECRET KEY'" >> venv/bin/activate
echo "export DB_USERNAME='THE DB USERNAME'" >> venv/bin/activate
echo "export DB_PASSWORD='THE DB PASSWORD'" >> venv/bin/activate
echo "export DB_HOST_PORT='THE DB HOST PORT'" >> venv/bin/activate

source venv/bin/activate
```

#### Running The Application on Local Server
Make sure you successfully completed the **First Time Setup**  and **Setting Up Sendgrid API_KEY**
steps before runing the application.
```bash
python3 run.py
```
visit: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)


#### Deactivating The Virtual Enviroment
```
deactivate
```

#### Activating The Virtual Enviroment and Running the App
```bash
cd TwitterLite
source venv/bin/activate
python3 run.py
```

## Style guide
  [PEP style guide.](https://www.python.org/dev/peps/pep-0008/)

## Project Structure
```
.
├── app
│   ├── static               
│   ├── templates
|   ├── .editorconfig
│   ├── views.py
|   ├── models.py
│   └── utils.py             
├── .gitignore
├── README.md
├── run.py
└── requirements.txt
```


## Contributers:
* [Bheki](https://github.com/BhekimpiloNdhlela)
* [David](https://github.com/Davidpcw)
* [Keanu](https://github.com/keanuDamon)
* [Klensch](https://github.com/KlenschLucas)
* [Nishaat](https://github.com/stress-princess)
* [Tahir](https://github.com/Hououin47)
