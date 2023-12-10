from setup import db, ma

class Entity(db.Model):
    __tablename__= "entities"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    type = db.Column(db.String())
    description = db.Column(db.String())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    events = db.relationship(
        "Event",
        back_populates="entities"
    )

# Schema
class EntitySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "type", "description", "user_id")

entity_schema = EntitySchema()

entities_schema = EntitySchema(many=True)
