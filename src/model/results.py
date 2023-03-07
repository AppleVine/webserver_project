from app import db


class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)

    # product_code = db.Column(
    # db.Integer(), 
    # db.ForeignKey("products.id"), 
    # nullable=False
    # )
    # product = db.relationship('Product', backref='results')
    product_code = db.Column(db.Integer(), nullable=False)

    staff_id = db.Column(
        db.Integer(), 
        db.ForeignKey("users.id"), 
        nullable=False
        )
    user = db.relationship('User', backref='results')

    specific_gravity = db.Column(db.Float(1, 2), nullable=False)
    pH = db.Column(db.Float(1, 14), nullable=False)
    reserve_alkalinity = db.Column(db.Float(1, 16), nullable=False)
    water_content = db.Column(db.Float(0, 5), nullable=False)
    test_time_date = db.Column(db.String(15), nullable=False)


   
    