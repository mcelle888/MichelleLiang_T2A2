from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ
from marshmallow.exceptions import ValidationError

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')

db = SQLAlchemy(app, session_options={"expire_on_commit": False})
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# Error handling

@app.errorhandler(401)
def unauthorized(err):
    return {'Error': 'Unauthorised Access'}

@app.errorhandler(ValidationError)
def validation_error(err):
    return {'Error': err.messages}

@app.errorhandler(KeyError)
def key_error(e):
    return jsonify({'Error': f'The field {e} is missing'}), 400