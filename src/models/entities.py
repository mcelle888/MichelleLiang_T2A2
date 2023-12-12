from setup import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

VALID_TYPES = ('planet', 'star')

class Entity(db.Model):
    __tablename__= "entities"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(), nullable = False)
    type = db.Column(db.String(), nullable = False)
    description = db.Column(db.String())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

# Schema
class EntitySchema(ma.Schema):

    type = fields.String(valide = OneOf(VALID_TYPES))
    class Meta:
        fields = ("id", "name", "type", "description", "user_id")

entity_schema = EntitySchema()

entities_schema = EntitySchema(many=True)
