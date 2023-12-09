from main import ma

class EntitySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "type", "events", "description")

entity_schema = EntitySchema()

entities_schema = EntitySchema(many=True)
