from main import db
from flask import Blueprint
from main import bcrypt
from models.diaries import Diary
from models.users import User
from datetime import date

db_commands = Blueprint("db", __name__)


@db_commands .cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands .cli.command("seed")
def seed_db():

# Creating users 
    admin_user = User(
        email = "admin@email.com",
        f_name = "Admin",
        password = bcrypt.generate_password_hash("password123").decode("utf-8"),
        admin = True,
        phone = 61429928942
    )
    db.session.add(admin_user)

    user1 = User(
        email = "jess@email.com",
        f_name = "Jess",
        password = bcrypt.generate_password_hash("123456").decode("utf-8"),
        phone = 61412111111
    )
    db.session.add(user1)
    
    user2 = User(
        email = "jay@email.com",
        f_name = "Jay",
        password = bcrypt.generate_password_hash("123456").decode("utf-8"),
        phone = 61410000121
    )
    db.session.add(user2)


    db.session.commit()

    # Creating diary entries
    diary1 = Diary(
        title = "Jupitar",
        description = "Caught Jupitar during setset at 7pm today",
        date = date.today(),
        user_id = user1.id
    )
    db.session.add(diary1)

    diary2 = Diary(
        title = "Meteor Shower",
        description = "Light meteor shower west of sky at 1am",
        date = date.today(),
        user_id = user2.id

    )

    db.session.add(diary2)


    # commit the changes
    db.session.commit()
    print("Table seeded")

@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")