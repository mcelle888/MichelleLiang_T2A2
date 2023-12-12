from setup import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class Diary(db.Model):
    __tablename__= "diaries"

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.Date())

    # Foreign key to establish relationship with users
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # SQLAlchemy relatinship which nests an instance of a user model in diary
    user = db.relationship("User", back_populates="diaries")

# Schema
class DiarySchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['password', 'phone', 'admin'])
    
    date = fields.String(required=True, validate=
        Regexp('^(?:(?:19|20)\d\d)-(?:0[1-9]|1[0-2])-(?:0[1-9]|1\d|2[0-8])$|^(?:(?:19|20)\d\d)-(?:0[13-9]|1[0-2])-(?:29|30)$|^(?:(?:19|20)(?:0[48]|[2468][048]|[13579][26]))-(?:0[1-9]|1[0-2])-29$', error='Invalid date/format, please enter: yyyy-mm-dd')
    )

    class Meta:
        fields = ("id", "title", "description", "date", "user_id", "user")

diary_schema = DiarySchema()

diaries_schema = DiarySchema(many=True)
