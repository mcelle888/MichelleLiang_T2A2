from flask import Blueprint, jsonify, request, abort
from setup import db, bcrypt
from models.users import User, user_schema, UserSchema
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from authorise import authorise
 
user_bp = Blueprint('user', __name__, url_prefix="/user")

# Route to sign up: /user/signup
@user_bp.route("/signup", methods=["POST"])
def user_register():
    try:
        user_fields = user_schema.load(request.json)
        stmt = db.select(User).filter_by(email=user_fields["email"])
        user = db.session.scalar(stmt)
        if user:
            return abort(400, description="Email is in use, please try again")
        user = User()
        user.email = user_fields["email"]
        user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
        user.admin = False
        user.phone = user_fields["phone"]
        user.name = user_fields["name"]
        db.session.add(user)
        db.session.commit()
        expiry = timedelta(hours=5)
        access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

        return jsonify({"user_email":user.email, "name": user.name, "phone": user.phone, "token": access_token }), 201
    except IntegrityError:
        return {"Error": "Email address already in use"}, 409
    
# Route to sign in
@user_bp.route("/signin", methods=["POST"])
def user_signin():
    user_fields = UserSchema(exclude=["phone", "name"]).load(request.json)
    stmt = db.select(User).filter_by(email=user_fields["email"])
    user = db.session.scalar(stmt)
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return {"error": "Invalid Email or Password"}, 401
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    return jsonify({"user":user.email, "token": access_token })

# Route to delete

@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()

def delete_user(user_id):

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if not user:
        return abort(400, description= "User doesn't exist")
    
    authorise()
        
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))


