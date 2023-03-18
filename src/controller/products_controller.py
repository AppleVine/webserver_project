from flask import Blueprint, request
from model.product import Product
from schema.products_schema import products_schema, product_schema
from app import db
from flask_jwt_extended import jwt_required,  get_jwt
from sqlalchemy.exc import IntegrityError

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
# Returns all columns of Products.
# SQL: SELECT * FROM products;


@product.get("/<int:id>")
@jwt_required()
def get_product(id):
    product = Product.query.get(id)
    current_user_claims = get_jwt()
    user_role = current_user_claims.get('role')
    # Returns the column that's id matches the id provided.
    # SQL: SELECT * FROM products WHERE id = [id];

    if user_role != "lab":
        return {"message": "You do not have authorization to view product information."}, 403

    if not product:
            return {"message": "This product does not exist."}, 403
    
    return product_schema.dump(product)    


@product.post("/")
@jwt_required()
def create_product():
    current_user_claims = get_jwt()
    user_role = current_user_claims.get('role')
    
    if user_role != "lab":
        return {"message": "You are not authorized to create a product."}, 403
    
    try:
        product_fields = product_schema.load(request.json)
        product = Product(**product_fields)
        db.session.add(product)
        db.session.commit()
        return {"result": product_schema.dump(product)}
    except IntegrityError:
        db.session.rollback()
        return {"message": "The product name must be unique."}, 400


@product.delete("/<int:id>")
@jwt_required()
def delete_product(id):
    try:
        current_user_claims = get_jwt()
        role = current_user_claims.get('role')
        product = Product.query.filter_by(id=id).first()
        # This searches Results and filters for the product that has the ID provided. 
        # SQL: SELECT * FROM products WHERE id = [id] LIMIT 1;

        if role != "lab":
            return {"message": "You do not have authorization to delete products."}, 403

        if not product:
            return {"message": "This product does not exist"}, 400
        
        db.session.delete(product)
        db.session.commit()
        return {"message": "This product has been deleted"}
    except IntegrityError:
        return {"msg": "This product has test results available, and therefore should not be deleted."}

@product.put("/<int:id>")
@jwt_required()
def update_product(id):
    current_user_claims = get_jwt()
    user_role = current_user_claims.get('role')
    product = db.session.query(Product).filter_by(id=id).first()
    # This searches Results and filters for the result that has the ID provided. 
    # SQL: SELECT * FROM results WHERE id = [id] LIMIT 1;

    if user_role != "lab":
        return {"message": "You are not authorized to update this product."}, 403

    if not product:
        return {"message": "There is no result with this id number."}, 400
    
    result_fields = product_schema.load(request.json)
    for field in result_fields:
            setattr(product, field, result_fields[field])
            db.session.commit()
    return {"updated product": product_schema.dump(product)}

