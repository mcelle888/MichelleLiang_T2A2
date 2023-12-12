from flask import Blueprint, jsonify, request, abort
from setup import db
from models.diaries import Diary, diary_schema, diaries_schema
from models.users import User
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
 

diaries_bp = Blueprint('diaries', __name__, url_prefix="/diaries")

# Route for getting a diary entry: /diaries/<int:id>
@diaries_bp.route("/<int:id>/", methods=["GET"])
@jwt_required()
def get_diary(id):
    user_id = get_jwt_identity()

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user:
        return abort(401, description="Invalid user")
    
    stmt = db.select(Diary).filter_by(id=id)
    diary = db.session.scalar(stmt)
    if not diary:
        return abort(400, description= "Diary not found")
    
    if diary.user_id != user.id and not user.admin:
        return abort(401)
    
    result = diary_schema.dump(diary)
    return jsonify(result)

# Route to retrieve diaries for a given user

@diaries_bp.route("/users/<int:id>", methods=["GET"])
@jwt_required()
def user_diaries(id):
    stmt = db.select(User).filter_by(id=id)
    user1 = db.session.scalar(stmt)

    if not user1:
        return abort(400, description = "User not found")
    
    # Authorisation: only allows users to access their own diaries
    jwt_user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)
    if user != user1:
        abort(401)

    

    stmt = db.select(Diary).filter_by(user_id=id)
    diary = db.session.scalar(stmt)
    if not diary:
        return abort(400, description= "No diary entries found for this user")

    result = diary_schema.dump(diary)
    return jsonify(result)   




# Route to post diary entry /

@diaries_bp.route("/", methods=["POST"])
@jwt_required()
def create_diary():

    diary_fields = diary_schema.load(request.json)

    user_id = get_jwt_identity()
    new_diary = Diary()
    new_diary.title = diary_fields["title"]
    new_diary.description = diary_fields["description"]
    new_diary.date = date.today()
    new_diary.user_id = user_id
    db.session.add(new_diary)
    db.session.commit()
 
    return jsonify(diary_schema.dump(new_diary))

# Route to update diary entry /diaries/
@diaries_bp.route("/<int:id>/", methods=["PUT", "PATCH"])
@jwt_required()
def update_diary(id):
    diary_fields = diary_schema.load(request.json)

    user_id = get_jwt_identity()

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if not user:
        return abort(401)

    stmt = db.select(Diary).filter_by(id=id)
    diary = db.session.scalar(stmt)

    if not diary:
        return abort(400, description= "Diary does not exist")

    diary.title = diary_fields["title"]
    diary.description = diary_fields["description"]
    diary.date = date.today()

    # Diary can only be updated by author
    if diary.user_id != user.id and not user.admin:
        return abort(401)
    db.session.commit()
    return jsonify(diary_schema.dump(diary))


# Route method to delete a diary entry

@diaries_bp.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_diary(id):
    user_id = get_jwt_identity()

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user:
        return abort(401, description="Invalid user")

    stmt = db.select(Diary).filter_by(id=id)
    diary = db.session.scalar(stmt)

    if not diary:
        return abort(400, description= "Diary doesn't exist")
    
    if diary.user_id != user.id and not user.admin:
        return abort(401)
        
    
    db.session.delete(diary)
    db.session.commit()
    return jsonify(diary_schema.dump(diary))