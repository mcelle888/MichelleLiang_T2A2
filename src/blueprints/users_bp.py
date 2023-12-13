from flask import Blueprint, jsonify, request, abort
from setup import db, bcrypt
from models.users import User, UserSchema, user_schema
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.exc import IntegrityError
from authorise import authorise

# users blueprint registered in app.py and sets url prefix 
user_bp = Blueprint('user', __name__, url_prefix="/user")


# Route to sign up: /user/signup/
@user_bp.route("/signup", methods=["POST"])
def user_register():
    # checks if user is already registered and if not creates a new entry
    try:
        user_fields = user_schema.load(request.json)

        stmt = db.select(User).filter_by(email=user_fields["email"])
        user = db.session.scalar(stmt)

        user = User()
        user.email = user_fields["email"]
        user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
        user.admin = False
        user.phone = user_fields["phone"]
        user.name = user_fields["name"]

        # add and commits new user
        db.session.add(user)
        db.session.commit()
        expiry = timedelta(hours=5)
        access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

        return jsonify({"user_email":user.email, "name": user.name, "phone": user.phone, "token": access_token }), 201
    except IntegrityError:
        return {"Error": "Email address already in use"}, 409
    

# Route to sign in: /user/signin/
@user_bp.route("/signin", methods=["POST"])
def user_signin(): 

    # finds a matching entry in the database
    user_fields = UserSchema(exclude=["phone", "name"]).load(request.json)
    stmt = db.select(User).filter_by(email=user_fields["email"])
    user = db.session.scalar(stmt)

    # if no match, an error is returned
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return {"error": "Invalid Email or Password"}, 401
    
    # else token is created and email and token is returned
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    return jsonify({"user":user.email, "token": access_token })


# Route to delete: /user/<int:id>
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()

def delete_user(user_id):
    # finds user id based on user_id given in url, if not found, returns error
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if not user:
        return abort(400, description= "User doesn't exist")
    
    # checks if user is admin
    authorise()

    # if admin passes, deletes entry and commits
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))


