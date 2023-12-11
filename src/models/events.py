from setup import db, ma

class Event(db.Model):
    __tablename__= "events"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    month = db.Column(db.String())
    entity_id = db.Column(db.Integer, db.ForeignKey("entities.id"))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class EventSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "month", "entity_id")

event_schema = EventSchema()

events_schema = EventSchema(many=True)