from flask import Blueprint
from app import db
from model.user import User

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
        lab_permission = True
    )
    user2 = User(
        email = "johnsemail@email.com",
        username = "JohnsUsername", 
        password = "Johnspassword",
        name = "John",
        lab_permission = False
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    print("tables seeded")