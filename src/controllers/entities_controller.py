from flask import Blueprint, jsonify, request, abort
from main import db
from models.entities import Entity
from models.users import User
from schemas.entity_schema import entity_schema, entities_schema
from flask_jwt_extended import jwt_required, get_jwt_identity


entities = Blueprint('entities', __name__, url_prefix="/entities")

# Route for getting a list of all the entities: /entities>
@entities.route("/", methods=["GET"])
@jwt_required()
def get_entities():
    stmt = db.select(Entity)
    entities = db.session.scalars(stmt).all()
    
    result = entities_schema.dump(entities)
    return jsonify(result)

# Route for filtering entities (e.g. get a list of all stars or a list of all planets)
@entities.route("/search", methods=["GET"])
@jwt_required()
def search_entities():

    entity_list = []

    if request.args.get('type'):
        stmt = db.select(Entity).filter_by(type= request.args.get('type'))
        entity_list = db.session.scalars(stmt)

    result = entities_schema.dump(entity_list)
    # return the data in JSON format
    return jsonify(result)

# Route to post a new entity (for admins only)

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