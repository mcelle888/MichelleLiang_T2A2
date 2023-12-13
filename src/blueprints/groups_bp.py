from flask import Blueprint, jsonify, request, abort
from setup import db
from models.groups import Group, group_schema, groups_schema
from models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity


groups_bp = Blueprint('groups', __name__, url_prefix="/groups")

# Get a list of groups: /groups/
@groups_bp.route("/", methods=["GET"])
@jwt_required()
def get_group():

    # selects all the groups available from class Group
    stmt = db.select(Group)
    groups = db.session.scalars(stmt).all()
    
    # converts to JSON objects to return
    result = groups_schema.dump(groups)
    return jsonify(result)


# Get a list of members of a specific group meeting: /groups/<int:id>/
@groups_bp.route("/<int:id>/", methods=["GET"])
@jwt_required()
def get_one_group(id):

    # selects matching group id entry in database
    stmt = db.select(Group).filter_by(meeting_id=id)
    groups = db.session.scalars(stmt)

    # if no match, an error is returned
    if not groups:
        return abort(400, description= "Meeting not found")
    
    # else token is created and email and token is returned
    result = groups_schema.dump(groups)
    return jsonify(result)


# Route to allow user to add themselves to a group meeting: /groups/
@groups_bp.route("/", methods=["POST"])
@jwt_required()
def create_group():
    # loads group marshmallow schema
    group_fields = group_schema.load(request.json)
    
    # creates new entry with incoming data(meeting_id and user_id)
    user_id = get_jwt_identity()
    new_group = Group()
    new_group.meeting_id = group_fields["meeting_id"]
    new_group.user_id = user_id

    # adds and commits changes
    db.session.add(new_group)
    db.session.commit()

    # returns new meeting details as JSON object
    return jsonify(group_schema.dump(new_group))



# Route to allow user to remove themselves from a group meeting: /groups/<int:id>/
@groups_bp.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_group(id):

    # checks user id 
    user_id = get_jwt_identity()

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    # finds group_id from Group class. 
    stmt = db.select(Group).filter_by(id=id)
    group = db.session.scalar(stmt)
    
    # if group does not exist, returns error
    if not group:
        return abort(400, description= "Group doesn't exist")

    # if user is not admin or owns the entry, aborts and returns error
    if group.user_id != user.id and not user.admin:
        return abort(401, description="Unauthorised User")
    
    # else delete and commit changes
    db.session.delete(group)
    db.session.commit()

    # returns JSON object of deleted meeting
    return jsonify(group_schema.dump(group))

