from setup import db, bcrypt
from flask import Blueprint
from models.diaries import Diary
from models.users import User
from models.meetings import Meeting
from models.entities import Entity
from models.events import Event
from models.groups import Group
from datetime import date
from pandas import Timestamp

db_commands = Blueprint('db', __name__)

# To create tables
@db_commands.cli.command("create")
def create_db():
    db.drop_all()
    db.create_all()
    print("Tables created")

@db_commands.cli.command("seed")
def seed_db():

# Creating users to seed the database
    user0 = User(
        email = "admin@email.com",
        name = "Admin",
        password = bcrypt.generate_password_hash("password123").decode("utf-8"),
        admin = True,
        phone = 61429928942,
        
    )
    db.session.add(user0)

    user1 = User(
        email = "jess@email.com",
        name = "Jess",
        password = bcrypt.generate_password_hash("abcdefg").decode("utf-8"),
        phone = 61412111111,
        admin = False
    )
    db.session.add(user1)
    
    user2 = User(
        email = "jay@email.com",
        name = "Jay",
        password = bcrypt.generate_password_hash("123456").decode("utf-8"),
        phone = 61410000121,
        admin = False
    )
    db.session.add(user2)

    user3 = User(
        email = "jasmine@email.com",
        name = "Jasmine",
        password = bcrypt.generate_password_hash("abcd1234").decode("utf-8"),
        phone = 61410122122,
        admin = False
    )
    db.session.add(user3)


    db.session.commit()

    # Creating diary entries for seeding
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

    # Creating meetings entries for seeding
    meeting1 = Meeting(
        title = "Welcome Meeting",
        description = "Come join our very first meeting, meet new members and introduce yourself!",
        date = Timestamp('2022-05-08'),
        time = "12pm",
        location = "Melbourne",
        leader_id = user0.id
    )
    db.session.add(meeting1)

    meeting2 = Meeting(
        title = "Comet Hale Sighting",
        description = "Comet Hale is visiting the southern skies next week, come join the group viewing!",
        date = Timestamp('2023-12-29'),
        time = "11pm",
        location = "Melbourne",
        leader_id = user0.id
    )
    db.session.add(meeting2)
    db.session.commit()
    # Creating celestial entity entries for seeding
    entity1 = Entity(
        name = "Mercury",
        description = "Closest planet to the sun and only slightly bigger than our moon. The planet is covered in impact craters. Temperatures are extremely hot during the day due to is proximity to the Sun but also extremely cold at night due to the lack of atmosphere.",
        type = "planet",
        user_id = user0.id
    )
    db.session.add(entity1)

    entity2 = Entity (
        name = "Venus",
        description = "Second planet from the sun and named after the goddess of love, venus is the hottest planet in our solar system due to it's close proximity to Earth and its thick atmosphere made up of CO2 and greenhouse gases. It features a rocky terrain with volcanoes and is often referred to as Earth's sister due to it's similar size.",
        type = "planet",
        user_id = user0.id
    )
    db.session.add(entity2)

    entity3 = Entity (
        name = "Mars",
        description = "Fourth planet from the sun with a rocky terrain and half the size of Earth. Mars is has a thin atmosphere however the surface of the planet is rather inactive and covered in rust which gives the planet its famous red tinge.",
        type = "planet",
        user_id = user0.id
    )
    db.session.add(entity3)

    entity4 = Entity (
        name = "Jupitar",
        description = "The largest planet in our solar system and covered in stripes and spots (active storms!). The most famous spot, called the red spot is located towards the bottom of the planet. Jupitar is a gas giant with rings (difficult to see unfortunately) and a heavy atmosphere",
        type = "planet",
        user_id = user0.id
    )
    db.session.add(entity4)

    entity5 = Entity (
        name = "Betelgeuse",
        description = "A red super giant star (764 times bigger than our sun!) in the shoulder of constellation Orion. One of the brightest stars viewable with the naked eye.",
        type = "star",
        user_id = user0.id
    )
    db.session.add(entity5)

    entity5 = Entity (
    name = "Sirius",
    description = "Greek for glowing or scorching, 'sirius' is the name of the brightest star in our skies. It is a binary star with Sirus A being the star we can see from Earth and its companion, Sirius B, 2000x less dimmer and therefore invisible to the unaided eye.",
    type = "star",
        user_id = user0.id
    )
    db.session.add(entity5)

# Creating events for seeding
    event1 = Event(
        name = "Mercury",
        description = "Viewable towards the Eastern horizon, in the early hours of dawn, an hour before the sun rises on the horizon. Greatest elongation will occur on the 13th where it will rise 90 minutes before the sun ",
        month = "January",
        entity_id = 1,
        user_id = user0.id 
    )
    db.session.add(event1)


    event2 = Event(
        name = "Betelgeuse",
        description = "April will be the brightest month to see this star",
        month = "April",
        entity_id = 5,
        user_id = user0.id
    )
    db.session.add(event2)

    group1 = Group(
        user_id = 1,
        meeting_id = 1
    )
    db.session.add(group1)

    group2 = Group (
        user_id = 2,
        meeting_id = 1
    )
    db.session.add(group2)

    group3 = Group (
        user_id = 1,
        meeting_id = 2
    )
    db.session.add(group3)
    

    # Seeding
    db.session.commit()
    print("Table seeded")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")