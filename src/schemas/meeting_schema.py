from main import ma

class MeetingSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "date", "time", "location", "leader_id")

meeting_schema = MeetingSchema()

meetings_schema = MeetingSchema(many=True)
