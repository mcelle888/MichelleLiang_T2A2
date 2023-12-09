from main import db

class Entity(db.Model):
    __tablename__= "entities"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    type = db.Column(db.String())
    description = db.Column(db.String())
    events = db.relationship(
        "Event",
        back_populates="entities"
    )
 