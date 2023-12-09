from main import db

class Event(db.Model):
    __tablename__= "events"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    month = db.Column(db.String())
    entity_id = db.Column(db.Integer, db.ForeignKey("entities.id"))
    entities = db.relationship(
        "Entity",
        back_populates="events"
    )