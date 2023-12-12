from setup import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

VALID_MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')

class Event(db.Model):
    __tablename__= "events"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    month = db.Column(db.String())
    entity_id = db.Column(db.Integer, db.ForeignKey("entities.id"))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    entities = db.relationship("Entity",back_populates="events",cascade="all, delete")


class EventSchema(ma.Schema):
    month = fields.String(validate=OneOf(VALID_MONTHS))

    
    class Meta:
        fields = ("id", "name", "description", "month", "entity_id")

event_schema = EventSchema()

events_schema = EventSchema(many=True)