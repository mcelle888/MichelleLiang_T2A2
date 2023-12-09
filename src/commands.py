from main import db
from flask import Blueprint
from main import bcrypt
from models.diaries import Diary
from models.users import User
from models.meetings import Meeting
from datetime import date
from pandas import Timestamp

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
        password = bcrypt.generate_password_hash("abcdefg").decode("utf-8"),
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

    user3 = User(
        email = "jasmine@email.com",
        f_name = "Jasmine",
        password = bcrypt.generate_password_hash("abcd1234").decode("utf-8"),
        phone = 61410122122
    )
    db.session.add(user3)


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

    diary3 = Diary(
        title = "Missed  the eclipse",
        description = "Late night at the office, missed the event :(",
        date = date.today(),
        user_id = user3.id

    )

    db.session.add(diary3)

    # Creating meetings entries
    meeting1 = Meeting(
        title = "Welcome Meeting",
        description = "Come join our very first meeting, meet new members and introduce yourself!",
        date = Timestamp('2022-05-08'),
        time = "12pm",
        location = "Melbourne",
        user_id = user1.id
    )
    db.session.add(meeting1)

    meeting2 = Meeting(
        title = "Comet Hale Sighting",
        description = "Comet Hale is visiting the southern skies next week, come join the group viewing!",
        date = Timestamp('2023-12-29'),
        time = "11pm",
        location = "Melbourne",
        user_id = user2.id
    )
    db.session.add(meeting2)
    


    db.session.commit()
    print("Table seeded")

@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")