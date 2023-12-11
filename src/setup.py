from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ
from marshmallow.exceptions import ValidationError

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = environ.get('DB_URI')

db = SQLAlchemy(app, session_options={"expire_on_commit": False})
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# @app.errorhandler(401)
# def unauthorized(err):
#     return {'error': 'Unauthorised Access'}

@app.errorhandler(ValidationError)
def validation_error(err):
    return {'error': err.messages}
