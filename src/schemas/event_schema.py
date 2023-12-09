from main import ma

class EventSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "month", "entity_id")

event_schema = EventSchema()

events_schema = EventSchema(many=True)
