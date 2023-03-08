from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint

class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)

    product_code = db.Column(
    db.Integer(), 
    db.ForeignKey("products.id"), 
    nullable=False
    )
    product = db.relationship('Product', backref='results')

    staff_id = db.Column(
        db.Integer(), 
        db.ForeignKey("users.id"), 
        nullable=False
        )
    user = db.relationship('User', backref='results')

    specific_gravity = db.Column(db.Numeric(scale=3), CheckConstraint('specific_gravity >= 0.8 and specific_gravity <=2.0'), nullable=False)
    potential_hydrogen = db.Column(db.Numeric(scale=2), CheckConstraint('potential_hydrogen >= 1.0 and potential_hydrogen <=14.0'), nullable=False)
    reserve_alkalinity = db.Column(db.Numeric(scale=3), CheckConstraint('reserve_alkalinity >= 1.0 and reserve_alkalinity <=16.0'), nullable=False)
    water_content = db.Column(db.Numeric(scale=3), CheckConstraint('water_content >= 0.00 and water_content <=5.0'), nullable=False)
    test_time_date = db.Column(db.String(15), nullable=False)

