from main import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = True)
    phone = db.Column(db.String(), nullable = True)
    email = db.Column(db.String(), nullable = False, unique=True)
    password = db.Column(db.String(), nullable = False)
    admin = db.Column(db.Boolean(), default=False)
    diaries = db.relationship(
        "Diary",
        back_populates="user",
        cascade="all, delete"
    )
    meetings = db.relationship(
        "Meeting",
        back_populates="user",
        cascade="all, delete"
    )