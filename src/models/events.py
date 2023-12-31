from setup import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

# Validation for months column
VALID_MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')


# Create Event Model (SQLAlchemy)
class Event(db.Model):
    __tablename__= "events"

    # Primary key
    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.String())
    description = db.Column(db.String())
    month = db.Column(db.String())
    
    # Foreign key establishes relationship with users at database level
    entity_id = db.Column(db.Integer, db.ForeignKey("entities.id"))

    # SQL Alchemy relationships
    entities = db.relationship("Entity",back_populates="events",cascade="all, delete")

# Marshmallow Schemas for events table and validation
class EventSchema(ma.Schema):
    
    # month must be a valid month
    month = fields.String(validate=OneOf(VALID_MONTHS))

    class Meta:
        fields = ("id", "name", "description", "month", "entity_id")

event_schema = EventSchema()
events_schema = EventSchema(many=True)