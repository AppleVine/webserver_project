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
























# @result.post("/")
# @jwt_required()
# def create_result():
#     current_user_claims = get_jwt()
#     user_role = current_user_claims.get('role')
#     staff_id = current_user_claims.get('user_id')
#     usersname = current_user_claims.get('name')
#     if user_role != "lab":
#         return {"message": "You are not authorized to view all users information."}, 403
#     else:
#         result_fields = result_schema.load(request.json)
#         result = Result(**result_fields)
        
#         if result.staff_id != staff_id:
#             return {"message": "You do not have authorization to post on behalf of other users."}

#         else:
#             db.session.add(result)
#             db.session.commit()
            
#             return { "result": result_schema.dump(result),
#                     "staff_member": f"{usersname}"
#                     }


# @result.put("/<int:id>")
# @jwt_required()
# def update_result(id):
#     current_user_claims = get_jwt()
#     user_id = current_user_claims.get('user_id')   
#     result = db.session.query(Result).filter_by(id=id).first()
#     if result:
#         if result.staff_id == user_id:
#             result_fields = result_schema.load(request.json)
#             for field in result_fields:
#                 setattr(result, field, result_fields[field])
#             db.session.commit()
#             return {"updated result": result_schema.dump(result)}
#         else:
#             return {"message": "You are not authorized to update this result."}
#     else:
#         return {"message": "There is no result with this id number."}
        

# @result.delete("/<int:id>")
# @jwt_required()
# def delete_result(id):
#     current_user_claims = get_jwt()
#     role = current_user_claims.get('role')
#     result = Result.query.filter_by(id=id).first()
#     if role == "lab":
#         if result:
#             db.session.delete(result)
#             db.session.commit()
#             return {"message": "This result has been deleted"}
#         else:
#             return {"message": "This result does not exist"}
#     else:
#         return {"message": "You do not have authorization to delete results."}
