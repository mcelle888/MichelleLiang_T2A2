from flask import Blueprint, jsonify, request, abort
from setup import db, bcrypt
from models.users import User, user_schema
from datetime import timedelta
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

# Route to sign up: /auth/signup
@auth_bp.route("/signup", methods=["POST"])
def auth_register():
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
    return jsonify({"user_email":user.email, "name": user.name, "phone": user.phone, "token": access_token })

@auth_bp.route("/signin", methods=["POST"])
def auth_signin():
    user_fields = user_schema.load(request.json)
    stmt = db.select(User).filter_by(email=user_fields["email"])
    user = db.session.scalar(stmt)
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Username and password don't match")
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    return jsonify({"user":user.email, "token": access_token })


