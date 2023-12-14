from setup import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

# Create User Model (SQLAlchemy)
class User(db.Model):
    __tablename__ = "users"

    # Primary key
    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(), nullable = True)
    phone = db.Column(db.String())
    email = db.Column(db.String(), nullable = False, unique=True)
    password = db.Column(db.String(), nullable = False)
    admin = db.Column(db.Boolean(), default=False)

    # SQL Alchemy relationships
    diaries = db.relationship("Diary", back_populates="user", cascade="all, delete")
    groups = db.relationship("Group",back_populates="user", cascade="all, delete")
    meetings = db.relationship("Meeting",back_populates="user",cascade="all, delete")

# Marshmallow Schemas for users table with validation
class UserSchema(ma.Schema):
    email = fields.Email(required = True)

    # name must not be empty
    name = fields.String(required = True, validate = Length(min = 1, error = 'Name must not be empty'))
    # password must be a minimum of 6 characters
    password = fields.String(required = True, validate = Length(min = 6, error = 'Password must have a minimum of 6 characters'))
    # phone must not be empty and must only contain numbers
    phone = fields.String(required=True, validate=And(
        Regexp('^[0-9]*$', error='Phone number must contain only numbers'),
        Length(min = 1, error='Phone number must not be empty')
                        ))
    
    class Meta:
        model = User
        fields = ("email", "name", "password", "admin", "phone")  

user_schema = UserSchema()
users_schema = UserSchema(many=True)

