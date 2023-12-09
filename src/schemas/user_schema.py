from main import ma
from models.users import User
from marshmallow.validate import Length

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("email", "name", "password", "admin")  
        password = ma.String(validate=Length(min=5))

user_schema = UserSchema()
users_schema = UserSchema(many=True)