from setup import db, ma
from marshmallow import fields
# from marshmallow.validate import OneOf, Regexp, Length, And

class Meeting(db.Model):
    __tablename__= "meetings"

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.Date())
    time = db.Column(db.String())
    location = db.Column(db.String())

    leader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    groups = db.relationship("Group",back_populates="meetings",cascade="all, delete")


class MeetingSchema(ma.Schema):
    groups = fields.Nested('GroupSchema')
    class Meta:
        fields = ("id", "title", "description", "date", "time", "location", "leader_id", "groups_id")

meeting_schema = MeetingSchema()

meetings_schema = MeetingSchema(many = True)

