from main import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    f_name = db.Column(db.String(), nullable = False)
    phone = db.Column(db.Integer(), nullable = True)
    email = db.Column(db.String(), nullable = False, unique=True)
    password = db.Column(db.String(), nullable = False)
    admin = db.Column(db.Boolean(), default=False)
    diaries = db.relationship(
        "Diary",
        back_populates="user",
        cascade="all, delete"
    )