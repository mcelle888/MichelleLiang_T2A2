from setup import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

# Create Meeting Model (SQLAlchemy)
class Meeting(db.Model):
    __tablename__= "meetings"

    # Primary key
    id = db.Column(db.Integer,primary_key=True)

    title = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.Date())
    time = db.Column(db.String())
    location = db.Column(db.String())

    # Foreign key establishes relationship with users on database level
    leader_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # SQL Alchemy relationships
    groups = db.relationship("Group",back_populates="meetings",cascade="all, delete")
    user = db.relationship("User",back_populates="meetings",cascade="all, delete")

# Marshmallow Schemas for meetings table with validation
class MeetingSchema(ma.Schema):
    groups = fields.Nested('GroupSchema')

    # date must be correct format yyyy/mm/dd
    date = fields.String(required=True, validate=
        Regexp('^(?:(?:19|20)\d\d)-(?:0[1-9]|1[0-2])-(?:0[1-9]|1\d|2[0-8])$|^(?:(?:19|20)\d\d)-(?:0[13-9]|1[0-2])-(?:29|30)$|^(?:(?:19|20)(?:0[48]|[2468][048]|[13579][26]))-(?:0[1-9]|1[0-2])-29$', error='Invalid date/format, please enter: yyyy-mm-dd')
    )
    
    class Meta:
        fields = ("id", "title", "description", "date", "time", "location", "leader_id", "groups_id")

meeting_schema = MeetingSchema()
meetings_schema = MeetingSchema(many = True)

