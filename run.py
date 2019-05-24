from app import *
import os

if __name__ == '__main__':
    app.secret_key = os.environ.get('SECRET_KEY')
    app.run(host='127.0.0.1', port=5000, debug=True)