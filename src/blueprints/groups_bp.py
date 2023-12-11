from flask import Blueprint, jsonify, request, abort
from setup import db
from models.groups import Group, group_schema, groups_schema
from models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity


groups_bp = Blueprint('groups', __name__, url_prefix="/groups")

# Get a list of groups
@groups_bp.route("/", methods=["GET"])
@jwt_required()
def get_group():
    stmt = db.select(Group)
    groups = db.session.scalars(stmt).all()
    
    result = groups_schema.dump(groups)
    return jsonify(result)

# Get a list of members of a specific group meeting

@groups_bp.route("/<int:id>/", methods=["GET"])
@jwt_required()
def get_one_group(id):
    stmt = db.select(Group).filter_by(meeting_id=id)
    groups = db.session.scalars(stmt)

    if not groups:
        return abort(400, description= "Meeting not found")
    
    result = groups_schema.dump(groups)
    return jsonify(result)


# Route to allow user to add themselves to a group meeting
@groups_bp.route("/", methods=["POST"])
@jwt_required()
def create_group():

    group_fields = group_schema.load(request.json)

    user_id = get_jwt_identity()
    new_group = Group()
    new_group.meeting_id = group_fields["meeting_id"]
    new_group.user_id = user_id
    db.session.add(new_group)
    db.session.commit()

    return jsonify(group_schema.dump(new_group))