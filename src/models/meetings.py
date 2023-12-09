from main import db

class Meeting(db.Model):
    __tablename__= "meetings"

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.Date())
    time = db.Column(db.String())
    location = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(
        "User",
        back_populates="meetings"
    )

