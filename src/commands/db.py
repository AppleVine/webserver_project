from flask import Blueprint
from app import db
from model.user import User
from model.results import Result

db_cmd = Blueprint("db", __name__)

@db_cmd.cli.command('create')
def create_db():
    db.create_all()
    print("Tables are created.")

@db_cmd.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables are dropped.")


@db_cmd.cli.command('seed')
def seed_db():
    user1 = User(
        email = "jakebemail@email.com",
        username = "JakebsUsername", 
        password = "jakebspassword",
        name = "Jakeb",
        role = "lab"
    )
    user2 = User(
        email = "johnsemail@email.com",
        username = "JohnsUsername", 
        password = "Johnspassword",
        name = "John",
        role = None
    )

    results1 = Result(
        product_code = 1,
        staff_id = 1,
        specific_gravity = 1.81,
        pH = 13,
        reserve_alkalinity = 8.2,
        water_content = 4.32,
        test_time_date = "12pm 13/04/22"
    )

    results2 = Result(
        product_code = 2,
        staff_id = 2,
        specific_gravity = 1.41,
        pH = 4,
        reserve_alkalinity = 4.2,
        water_content = 3.44,
        test_time_date = "1pm 15/04/22"
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(results1)
    db.session.add(results2)
    db.session.commit()
    print("tables seeded")
