from flask import Blueprint, jsonify, request, abort
from setup import db
from models.diaries import Diary, diary_schema, diaries_schema
from models.users import User
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
 
# diaries blueprint registered in app.py and sets url prefix 
diaries_bp = Blueprint('diaries', __name__, url_prefix="/diaries")

# Route for getting a diary entry: /diaries/<int:id>/
@diaries_bp.route("/<int:id>/", methods=["GET"])
@jwt_required()
def get_diary(id):
    user_id = get_jwt_identity()

    # checks user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user:
        return abort(401, description="Invalid user")
    
    # # selects matching diary id entry in database
    stmt = db.select(Diary).filter_by(id=id)
    diary = db.session.scalar(stmt)

    # if no match, an error is returned
    if not diary:
        return abort(400, description= "Diary not found")
    
    # checks user is admin or owner of diary, if not abort
    if diary.user_id != user.id and not user.admin:
        return abort(401)
    
    # else return diary entry as a JSON object
    result = diary_schema.dump(diary)
    return jsonify(result)


# Route to retrieve diaries for a given user: /diaries/users/<int:id>/
@diaries_bp.route("/users/<int:id>", methods=["GET"])
@jwt_required()
def user_diaries(id):

    # checks user_id is valid
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

    
    # if diary entry belongs to user, finds matching entry 
    stmt = db.select(Diary).filter_by(user_id=id)
    diary = db.session.scalar(stmt)
    # if diary_id is not found, return error message
    if not diary:
        return abort(400, description= "No diary entries found for this user")

    # else return list of diary entries for the user as JSON objects
    result = diary_schema.dump(diary)
    return jsonify(result)   


# Route to post diary entry /diaries/
@diaries_bp.route("/", methods=["POST"])
@jwt_required()
def create_diary():
    # loads diary marshmallow schema
    diary_fields = diary_schema.load(request.json)

    # creates new entry with incoming data
    user_id = get_jwt_identity()
    new_diary = Diary()
    new_diary.title = diary_fields["title"]
    new_diary.description = diary_fields["description"]
    new_diary.date = date.today()
    new_diary.user_id = user_id

    # adds and commits changes
    db.session.add(new_diary)
    db.session.commit()
    
    # returns new meeting details as JSON object
    return jsonify(diary_schema.dump(new_diary))


# Route to update diary entry /diaries/<int:id>/
@diaries_bp.route("/<int:id>/", methods=["PUT", "PATCH"])
@jwt_required()
def update_diary(id):
    diary_fields = diary_schema.load(request.json)

    user_id = get_jwt_identity()

    # checks user identity through User class
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    # if no  user is found, error
    if not user:
        return abort(401)

    # searches for given diary_id in database
    stmt = db.select(Diary).filter_by(id=id)
    diary = db.session.scalar(stmt)

    # if no entry exists, returns an error
    if not diary:
        return abort(400, description= "Diary does not exist")

    # else updates existing entry 
    diary.title = diary_fields["title"]
    diary.description = diary_fields["description"]
    diary.date = date.today()

    # if user is not admin or owner of diary, error returns
    if diary.user_id != user.id and not user.admin:
        return abort(401)
    
    # else changes are commited and JSON object is returned
    db.session.commit()
    return jsonify(diary_schema.dump(diary))


# Route method to delete a diary entry: /diaries/<int:id>/
@diaries_bp.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_diary(id):

     # checks user id
    user_id = get_jwt_identity()

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user:
        return abort(401, description="Invalid user")

    # finds diary_id_id from Diary class. 
    stmt = db.select(Diary).filter_by(id=id)
    diary = db.session.scalar(stmt)

    # if diary does not exist, returns error
    if not diary:
        return abort(400, description= "Diary doesn't exist")

    # if user is not admin or owns the meeting (leader), aborts and returns error
    if diary.user_id != user.id and not user.admin:
        return abort(401)
        
    # else delete and commit changes   
    db.session.delete(diary)
    db.session.commit()
    
    # returns JSON object of deleted meeting
    return jsonify(diary_schema.dump(diary))