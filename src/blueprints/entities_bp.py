from flask import Blueprint, jsonify, request, abort
from setup import db
from models.entities import Entity, entities_schema, entity_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from authorise import authorise


entities_bp = Blueprint('entities', __name__, url_prefix="/entities")

# Route for getting a list of all the entities: /entities>
@entities_bp.route("/", methods=["GET"])
@jwt_required()
def get_entities():
    stmt = db.select(Entity)
    entities = db.session.scalars(stmt).all()
    
    result = entities_schema.dump(entities)
    return jsonify(result)

# Route for filtering entities (e.g. get a list of all stars or a list of all planets)
@entities_bp.route("/search", methods=["GET"])
@jwt_required()
def search_entities():

    entity_list = []

    if request.args.get('type'):
        stmt = db.select(Entity).filter_by(type= request.args.get('type'))
        entity_list = db.session.scalars(stmt)

    result = entities_schema.dump(entity_list)
    return jsonify(result)

# Route to post a new entity (admin only)
@entities_bp.route("/", methods=["POST"])
@jwt_required()
def create_entity():

    entity_fields = entity_schema.load(request.json)

    user_id = get_jwt_identity() 
    new_entity = Entity()
    new_entity.name = entity_fields["name"]
    new_entity.description = entity_fields["description"]
    new_entity.type = entity_fields["type"]
    new_entity.user_id = user_id

    if new_entity:
        authorise()

        db.session.add(new_entity)
        db.session.commit()
        return jsonify(entity_schema.dump(new_entity))
    else:
        return {'Error': "Unauthorised Access" }
    
# Route to update a specific entity (admin only)
@entities_bp.route("/<int:id>/", methods=["PUT"])
@jwt_required()
def update_entity(id):
    entity_fields = entity_schema.load(request.json)

    stmt = db.select(Entity).filter_by(id=id)
    entity = db.session.scalar(stmt)

    if not entity:
        return abort(400, description= "Entity does not exist")

    entity.name = entity_fields["name"]
    entity.description = entity_fields["description"]
    entity.type = entity_fields["type"]

    if entity:
        authorise()
        db.session.commit()
        return jsonify(entity_schema.dump(entity))
    
# Route to delete an entity (admin only)
@entities_bp.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_entity(id):

    stmt = db.select(Entity).filter_by(id=id)
    entity = db.session.scalar(stmt)

    if not entity:
        return abort(400, description= "Entity doesn't exist")

    if entity:
        authorise()    
    
        db.session.delete(entity)
        db.session.commit()
        return jsonify(entity_schema.dump(entity))