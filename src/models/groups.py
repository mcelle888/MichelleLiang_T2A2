from setup import db, ma  
from marshmallow import fields

# Create Group Model (SQLAlchemy)
class Group(db.Model):
    __tablename__= "groups"

    # Primary key
    id = db.Column(db.Integer,primary_key=True)

    # Foreign keys establishes connection to users and meetings at the database level
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.id"), nullable=False)

    # SQL Alchemy relationships
    user = db.relationship("User", back_populates="groups")
    meetings = db.relationship("Meeting",back_populates="groups",cascade="all, delete")

# Marshmallow Schemas for groups table
class GroupSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['password','admin'])

    class Meta:
        fields = ("user_id", "meeting_id", "user")

group_schema = GroupSchema()
groups_schema = GroupSchema(many = True)
