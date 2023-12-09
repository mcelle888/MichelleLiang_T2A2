from flask import Blueprint, jsonify, request, abort
from main import db
from models.diaries import Diary
from models.users import User
from schemas.diary_schema import diary_schema, diaries_schema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity


diaries = Blueprint('diaries', __name__, url_prefix="/diaries")

# Route for getting a diary entry: /diaries/<int:id>
@diaries.route("/<int:id>/", methods=["GET"])
@jwt_required()
def get_diary(id):
    stmt = db.select(Diary).filter_by(id=id)
    diary = db.session.scalar(stmt)
    if not diary:
        return abort(400, description= "Diary not found")
    result = diary_schema.dump(diary)
    return jsonify(result)

# Route for getting diary entries from a particular user /diaries/user
@diaries.route("/user", methods = ["GET"])
@jwt_required()
def get_user_diary(): 
    user_id = get_jwt_identity()

    stmt = db.select(Diary).filter_by(user_id = user_id)
    diaries = db.session.scalars(stmt)

    result = diaries_schema.dump(diaries)
    return jsonify(result)

# Route to post diary entry /

@diaries.route("/", methods=["POST"])
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
@diaries.route("/<int:id>/", methods=["PUT"])
@jwt_required()
def update_diary(id):
    diary_fields = diary_schema.load(request.json)

    user_id = get_jwt_identity()

    stmt = db.select(Diary).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)

    if not user:
        return abort(401, description="Unauthorised User")
    


    stmt = db.select(Diary).filter_by(id=id)
    diary = db.session.scalar(stmt)

    if not diary:
        return abort(400, description= "Diary does not exist")

    diary.title = diary_fields["title"]
    diary.description = diary_fields["description"]
    diary.date = date.today()

    # Diary can only be updated by author
    if diary.user_id != user.id:
        return abort(401, description="Unauthorised User")

    db.session.commit()
    return jsonify(diary_schema.dump(diary))


# Route method to delete a diary entry

@diaries.route("/<int:id>/", methods=["DELETE"])
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
        return abort(401, description="Unauthorised User")
        
    

    db.session.delete(diary)
    db.session.commit()
    return jsonify(diary_schema.dump(diary))