import os

from flask_cors import CORS
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

# initialization
app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'lasijasdfkjhlsdkjlfadskjlfsdahjkl89pweffrtjawsoi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['PORT'] = os.environ['PORT'] if 'PORT' in os.environ else 8000


# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
