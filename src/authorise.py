from flask import abort
from flask_jwt_extended import get_jwt_identity
from models.users import User
from setup import db

# Admin only function
def authorise(user_id=None):
    jwt_user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)
    if not (user.admin or (user_id and jwt_user_id == user_id)):
        abort(401)

