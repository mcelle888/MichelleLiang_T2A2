from flask import Blueprint, jsonify, request, abort
from setup import db
from models.meetings import Meeting, meeting_schema, meetings_schema
from models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity

# meeting blueprint registered in app.py and sets url prefix 
meetings_bp = Blueprint('meetings', __name__, url_prefix="/meetings")


# Route for getting a list of all the meetings: /meetings/
@meetings_bp.route("/", methods=["GET"])
@jwt_required()
def get_meeting():
    
    # selects all the meetings available from class Meeting
    stmt = db.select(Meeting)
    meetings = db.session.scalars(stmt).all()
    
    # converts to JSON objects to return
    result = meetings_schema.dump(meetings)
    return jsonify(result)


# Route for details about the a specific meeting: /meetings/<int:id>/
@meetings_bp.route("/<int:id>/", methods=["GET"])
@jwt_required()
def get_one_meeting(id):

    # selects matching meeting id entry in database
    stmt = db.select(Meeting).filter_by(id=id)
    meeting = db.session.scalar(stmt)

    # if no match, an error is returned
    if not meeting:
        return abort(400, description= "Meeting not found")
    
    # else token is created and email and token is returned
    result = meeting_schema.dump(meeting)
    return jsonify(result)


# Route to edit a specific meeting: /meetings/<int:id>/
@meetings_bp.route("/<int:id>/", methods=["PUT", "PATCH"])
@jwt_required()

def update_one_meeting(id):
    meeting_fields = meeting_schema.load(request.json)

    user_id = get_jwt_identity()

    # checks user identity through User class
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # if no  user is found, error
    if not user:
        return abort(401, description="Unauthorised User")

    # searches for given meeting_id in database
    stmt = db.select(Meeting).filter_by(id=id)
    meeting = db.session.scalar(stmt)

    # if no entry exists, returns an error
    if not meeting:
        return abort(400, description= "Meeting does not exist")
  
    # else updates existing entry 
    meeting.title = meeting_fields["title"]
    meeting.description = meeting_fields["description"]
    meeting.date = meeting_fields["date"]
    meeting.location = meeting_fields["location"]
    meeting.time= meeting_fields["time"]
  
    # if user is not admin or owner of meeting (leader), error returns
    if meeting.leader_id != user.id and not user.admin:
        return abort(401, description="Unauthorised User")
    
    # else changes are committed. 
    db.session.commit()
    return jsonify(meeting_schema.dump(meeting))


# Route to create a new meeting entry: /meetings/

@meetings_bp.route("/", methods=["POST"])
@jwt_required()
def create_meeting():
    # loads meeting marshmallow schema
    meeting_fields = meeting_schema.load(request.json)

    # creates new entry with incoming data
    user_id = get_jwt_identity()
    new_meeting = Meeting()
    new_meeting.title = meeting_fields["title"]
    new_meeting.description = meeting_fields["description"]
    new_meeting.date = meeting_fields["date"]
    new_meeting.location = meeting_fields["location"]
    new_meeting.time= meeting_fields["time"]
    new_meeting.leader_id = user_id

    # adds and commits changes
    db.session.add(new_meeting)
    db.session.commit()

    # returns new meeting details as JSON object
    return jsonify(meeting_schema.dump(new_meeting))


# Route to delete a meeting entry: /meetings/<int:id>
@meetings_bp.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_meeting(id):

    # checks user id
    user_id = get_jwt_identity()

   
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user:
        return abort(401, description="Invalid user")

    # finds meeting_id from Meeting class. 
    stmt = db.select(Meeting).filter_by(id=id)
    meeting = db.session.scalar(stmt)

    # if meeting does not exist, returns error
    if not meeting:
        return abort(400, description= "Meeting doesn't exist")
    
    # if user is not admin or owns the meeting (leader), aborts and returns error
    if meeting.leader_id != user.id and not user.admin:
        return abort(401)
    
    # else delete and commit changes
    db.session.delete(meeting)
    db.session.commit()

    # returns JSON object of deleted meeting
    return jsonify(meeting_schema.dump(meeting))
