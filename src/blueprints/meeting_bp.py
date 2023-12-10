from flask import Blueprint, jsonify, request, abort
from setup import db
from models.meetings import Meeting, meeting_schema, meetings_schema
from models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity


meetings_bp = Blueprint('meetings', __name__, url_prefix="/meetings")



# Route for getting a list of all the meetings: /meetings>
@meetings_bp.route("/", methods=["GET"])
@jwt_required()
def get_meeting():
    stmt = db.select(Meeting)
    meetings = db.session.scalars(stmt).all()
    
    result = meetings_schema.dump(meetings)
    return jsonify(result)

# Route for details about the a specific meeting
@meetings_bp.route("/<int:id>/", methods=["GET"])
@jwt_required()
def get_one_meeting(id):
    stmt = db.select(Meeting).filter_by(id=id)
    meeting = db.session.scalar(stmt)
    if not meeting:
        return abort(400, description= "Meeting not found")
    result = meeting_schema.dump(meeting)
    return jsonify(result)

# Route to edit a specific meeting
@meetings_bp.route("/<int:id>/", methods=["PUT"])
@jwt_required()

def update_one_meeting(id):
    meeting_fields = meeting_schema.load(request.json)

    user_id = get_jwt_identity()

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if not user:
        return abort(401, description="Unauthorised User")

    stmt = db.select(Meeting).filter_by(id=id)
    meeting = db.session.scalar(stmt)

    if not meeting:
        return abort(400, description= "Meeting does not exist")
  
    meeting.title = meeting_fields["title"]
    meeting.description = meeting_fields["description"]
    meeting.date = meeting_fields["date"]
    meeting.location = meeting_fields["location"]
  
    if meeting.leader_id != user.id and not user.admin:
        return abort(401, description="Unauthorised User")
    db.session.commit()
    return jsonify(meeting_schema.dump(meeting))

