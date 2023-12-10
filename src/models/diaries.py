from main import db, ma

class Diary(db.Model):
    __tablename__= "diaries"

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.Date())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(
        "User",
        back_populates="diaries"
    )

# Schema
class DiarySchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "date", "user_id")

diary_schema = DiarySchema()

diaries_schema = DiarySchema(many=True)
