from setup import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

# Validation for type column
VALID_TYPES = ('planet', 'star')

# Create Entity Model (SQLAlchemy)
class Entity(db.Model):
    __tablename__= "entities"
    
    # Primary key
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(), nullable = False)
    type = db.Column(db.String(), nullable = False)
    description = db.Column(db.String())

    # SQL Alchemy relationships
    events = db.relationship("Event",back_populates="entities",cascade="all, delete")

# Marshmallow Schemas for entities table and validation
class EntitySchema(ma.Schema):

    # Type must be one of either planet or star
    type = fields.String(valide = OneOf(VALID_TYPES))
    class Meta:
        fields = ("id", "name", "type", "description")

entity_schema = EntitySchema()
entities_schema = EntitySchema(many=True)
