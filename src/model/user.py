from app import db
from sqlalchemy import CheckConstraint

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(30), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(20), default=None)
    __table_args__ = (
        CheckConstraint('length(email) >= 5'),
        CheckConstraint('length(username) >= 5'),
        CheckConstraint('length(password) >= 8'),
        CheckConstraint('length(name) >= 2'),
        CheckConstraint('length(role) >= 3'),
    )

   
    