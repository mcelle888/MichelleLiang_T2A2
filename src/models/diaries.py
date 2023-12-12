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

    class Meta:
        fields = ("id", "title", "description", "date", "user_id", "user")

diary_schema = DiarySchema()

diaries_schema = DiarySchema(many=True)
