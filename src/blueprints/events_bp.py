from flask import Blueprint, jsonify, request, abort
from setup import db
from models.events import Event, events_schema, event_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from authorise import authorise

# event blueprint registered in app.py and sets url prefix 
events_bp = Blueprint('events', __name__, url_prefix="/events")

# Route for getting a list of all the events: /events/
@events_bp.route("/", methods=["GET"])
@jwt_required()
def get_events():

    # selects all the events available from class Event
    stmt = db.select(Event)
    events = db.session.scalars(stmt).all()
    
    # converts to JSON objects to return
    result = events_schema.dump(events)
    return jsonify(result)


# Route for filtering events (e.g. get a list of events by month): /events/search?month=
@events_bp.route("/search", methods=["GET"])
@jwt_required()
def search_events():

    # Create an empty list
    event_list = []

    # search for matching month entries and add entries to list
    if request.args.get('month'):
        stmt = db.select(Event).filter_by(month=request.args.get('month'))
        event_list = db.session.scalars(stmt)

    # converts to JSON objects to return
    result = events_schema.dump(event_list)
    return jsonify(result)


# Route to post a new event (admin only): /events/
@events_bp.route("/", methods=["POST"])
@jwt_required()
def create_event():

    # loads events marshmallow schema
    event_fields = event_schema.load(request.json)

    # creates new entry with incoming data
    user_id = get_jwt_identity() 
    new_event = Event()
    new_event.name = event_fields["name"]
    new_event.description = event_fields["description"]
    new_event.month = event_fields["month"]
    new_event.entity_id = event_fields["entity_id"]
    new_event.user_id = user_id
    
    # checks if user is admin. if not return error
    if new_event:
        authorise()
        
    # else adds and commits the changes and returns event details as JSON object.
        db.session.add(new_event)
        db.session.commit()
        return jsonify(event_schema.dump(new_event))
    else:
        return {'Error': "Unauthorised Access" }
    

# Route to update a specific event (admin only): /events/<int:id>/
@events_bp.route("/<int:id>/", methods=["PUT", "PATCH"])
@jwt_required()
def update_event(id):

    # loads the events schema
    event_fields = event_schema.load(request.json)

    # finds the mataching event id in the databse
    stmt = db.select(Event).filter_by(id=id)
    event = db.session.scalar(stmt)

    # if event does not exist, abort
    if not event:
        return abort(400, description= "Event does not exist")

    # else update event details with given data
    event.name = event_fields["name"]
    event.description = event_fields["description"]
    event.month = event_fields["month"]
    event.event_id = event.id

    # if not admin, abort else commit session and return updated event details.
    if event:
        authorise()
        db.session.commit()
        return jsonify(event_schema.dump(event))
    

# Route to delete an event (admin only): /events/<int:id>
@events_bp.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_event(id):

    # finds event_id from Event class. 
    stmt = db.select(Event).filter_by(id=id)
    event = db.session.scalar(stmt)

    # if event does not exist, abort
    if not event:
        return abort(400, description= "Event doesn't exist")

    # else if not admin abort, else delete event and commit the change, returning deleted event as JSON object.
    if event:
        authorise()    
    
        db.session.delete(event)
        db.session.commit()
        return jsonify(event_schema.dump(event))