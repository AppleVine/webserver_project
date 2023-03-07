from app import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    product_name = db.Column(db.String(100), nullable=False, unique=True)
    product_description = db.Column(db.String(400))
    product_cost = db.Column(db.Float(10), nullable=False)


   
    