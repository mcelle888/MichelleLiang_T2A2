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

# Get a specific groups list

@groups_bp.route("/<int:id>/", methods=["GET"])
@jwt_required()
def get_one_group(id):
    stmt = db.select(Group).filter_by(meeting_id=id)
    groups = db.session.scalars(stmt)

    if not groups:
        return abort(400, description= "Meeting not found")
    
    result = groups_schema.dump(groups)
    return jsonify(result)