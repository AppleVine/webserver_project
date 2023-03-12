from flask import Blueprint, request
from model.product import Product
from schema.products_schema import products_schema, product_schema
from app import db
from flask_jwt_extended import jwt_required,  get_jwt


product = Blueprint('product', __name__, url_prefix='/products')


@product.get("/")
@jwt_required()
def get_products():
    current_user_claims = get_jwt()
    user_role = current_user_claims.get('role')
    if user_role == "lab":
        products = Product.query.all()
        return products_schema.dump(products)
    else:
        return {"message": "You do not have authorization to view all product information."}, 403


@product.get("/<int:id>")
@jwt_required()
def get_product(id):
    product = Product.query.get(id)
    current_user_claims = get_jwt()
    user_role = current_user_claims.get('role')
    if user_role == "lab":
        if product:
            return product_schema.dump(product)
        else:
            return {"message": "This product does not exist."}, 403
    else:
        return {"message": "You do not have authorization to view product information."}, 403


@product.post("/")
@jwt_required()
def create_product():
    current_user_claims = get_jwt()
    user_role = current_user_claims.get('role')
    if user_role != "lab":
        return {"message": "You are not authorized to create a product."}, 403
    else:
        product_fields = product_schema.load(request.json)
        product = Product(**product_fields)
        db.session.add(product)
        db.session.commit()
        return {"result": product_schema.dump(product)}


@product.delete("/<int:id>")
@jwt_required()
def delete_product(id):
    current_user_claims = get_jwt()
    role = current_user_claims.get('role')
    product = Product.query.filter_by(id=id).first()
    if role == "lab":
        if product:
            db.session.delete(product)
            db.session.commit()
            return {"message": "This product has been deleted"}
        else:
            return {"message": "This product does not exist"}, 400
    else:
        return {"message": "You do not have authorization to delete products."}, 403

