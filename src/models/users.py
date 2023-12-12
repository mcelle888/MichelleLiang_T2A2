from setup import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = True)
    phone = db.Column(db.String())
    email = db.Column(db.String(), nullable = False, unique=True)
    password = db.Column(db.String(), nullable = False)
    admin = db.Column(db.Boolean(), default=False)

    # SQL Alchemy relationship 
    diaries = db.relationship("Diary", back_populates="user", cascade="all, delete")
    groups = db.relationship("Group",back_populates="user", cascade="all, delete")
    meetings = db.relationship("Meeting",back_populates="user",cascade="all, delete")
    entities = db.relationship("Entity",back_populates="user",cascade="all, delete")


class UserSchema(ma.Schema):
    email = fields.Email(required = True)
    name = fields.String(required = True, validate = Length(min = 1, error = 'Name must not be empty'))
    password = fields.String(required = True, validate = Length(min = 6, error = 'Password must have a minimum of 6 characters'))
    phone = fields.String(required=True, validate=And(
        Regexp('^[0-9]*$', error='Phone number must contain only numbers'),
        Length(min = 1, error='Phone number must not be empty')
    ))
    class Meta:
        model = User
        fields = ("email", "name", "password", "admin", "phone")  

user_schema = UserSchema()
users_schema = UserSchema(many=True)

