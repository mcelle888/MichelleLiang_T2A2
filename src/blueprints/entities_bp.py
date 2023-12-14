from flask import Blueprint, jsonify, request, abort
from setup import db
from models.entities import Entity, entities_schema, entity_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from authorise import authorise

# entities blueprint registered in app.py and sets url prefix 
entities_bp = Blueprint('entities', __name__, url_prefix="/entities")

# Route for getting a list of all the entities: /entities/
@entities_bp.route("/", methods=["GET"])
@jwt_required()
def get_entities():

    # selects all the entities available from class Entity
    stmt = db.select(Entity)
    entities = db.session.scalars(stmt).all()
    
    # converts to JSON objects to return
    result = entities_schema.dump(entities)
    return jsonify(result)

# Route for filtering entities (e.g. get a list of entities by type): /entities/search?type=
@entities_bp.route("/search", methods=["GET"])
@jwt_required()
def search_entities():

    # Create an empty list
    entity_list = []

    # search for matching type entries and add entries to list
    if request.args.get('type'):
        stmt = db.select(Entity).filter_by(type= request.args.get('type'))
        entity_list = db.session.scalars(stmt)

    # converts to JSON objects to return
    result = entities_schema.dump(entity_list)
    return jsonify(result)


# Route to post a new entity (admin only): /entities/
@entities_bp.route("/", methods=["POST"])
@jwt_required()
def create_entity():

    # loads entities marshmallow schema
    entity_fields = entity_schema.load(request.json)

    # creates new entry with incoming data
    user_id = get_jwt_identity() 
    new_entity = Entity()
    new_entity.name = entity_fields["name"]
    new_entity.description = entity_fields["description"]
    new_entity.type = entity_fields["type"]

    # checks if user is admin. if not return error
    if new_entity:
        authorise()

        # else adds and commits the changes and returns entity details as JSON object.
        db.session.add(new_entity)
        db.session.commit()
        return jsonify(entity_schema.dump(new_entity))
    else:
        return {'Error': "Unauthorised Access" }
    

# Route to update a specific entity (admin only): /entities/<int:id>/
@entities_bp.route("/<int:id>/", methods=["PUT", "PATCH"])
@jwt_required()
def update_entity(id):
    # loads the entity schema
    entity_fields = entity_schema.load(request.json)

    # finds the mataching entity id in the databse
    stmt = db.select(Entity).filter_by(id=id)
    entity = db.session.scalar(stmt)

    # if entity does not exist, abort
    if not entity:
        return abort(400, description= "Entity does not exist")

    # else update entity details with given data
    entity.name = entity_fields["name"]
    entity.description = entity_fields["description"]
    entity.type = entity_fields["type"]

    # if not admin, abort. Else commit session and return updated entity details.
    if entity:
        authorise()
        db.session.commit()
        return jsonify(entity_schema.dump(entity))


# Route to delete an entity (admin only): /entities/<int:id>/
@entities_bp.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_entity(id):

    # finds entity_id from Entity class.
    stmt = db.select(Entity).filter_by(id=id)
    entity = db.session.scalar(stmt)

    # if entity does not exist, abort
    if not entity:
        return abort(400, description= "Entity doesn't exist")

    # else if not admin abort, else delete entity and commit the change, returning deleted event as JSON object.
    if entity:
        authorise()    
    
        db.session.delete(entity)
        db.session.commit()
        return jsonify(entity_schema.dump(entity))