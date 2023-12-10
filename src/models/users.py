from main import db, ma
from models.users import User
from marshmallow.validate import Length

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = True)
    phone = db.Column(db.String(), nullable = True)
    email = db.Column(db.String(), nullable = False, unique=True)
    password = db.Column(db.String(), nullable = False)
    admin = db.Column(db.Boolean(), default=False)
    diaries = db.relationship(
        "Diary",
        back_populates="user",
        cascade="all, delete"
    )
    meetings = db.relationship(
        "Meeting",
        back_populates="user",
        cascade="all, delete"
    )


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("email", "name", "password", "admin", "phone")  
        password = ma.String(validate=Length(min=5, error = "Password must be at least 5 characters"))

user_schema = UserSchema()
users_schema = UserSchema(many=True)