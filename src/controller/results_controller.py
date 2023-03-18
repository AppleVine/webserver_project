from flask import Blueprint, request
from model.user import User
from model.product import Product
from model.result import Result
from schema.results_schema import results_schema, result_schema, productresult_schema
from app import db
from flask_jwt_extended import jwt_required,  get_jwt
from sqlalchemy.exc import IntegrityError

result = Blueprint('result', __name__, url_prefix='/results')


@result.get("/")
def get_results():
    results = Result.query.all()
    return results_schema.dump(results)
# Returns all columns of Result.
# SQL: SELECT * FROM results;


@result.get("/<int:id>")
def get_result(id):
    result = Result.query.get(id)
    if result:
        return result_schema.dump(result)
    else:
        return {"message": "This result does not exist."}, 400
# Returns the column that's id matches the id provided.
# SQL: SELECT * FROM results WHERE id = [id];


@result.post("/")
@jwt_required()
def create_result():
    current_user_claims = get_jwt()
    user_role = current_user_claims.get('role')
    staff_id = current_user_claims.get('user_id')
    usersname = current_user_claims.get('name')
    
    if user_role != "lab":
        return {"message": "You are not authorized to create lab results."}, 403

    try:
        result_fields = result_schema.load(request.json)
        result = Result(**result_fields)
        product_id = result_fields.get("product_code")
        product_search = db.session.query(Product).filter_by(id=product_id).first()
        # This is to check that the product code the tester has provided exists in the database. It searches all in products for the product id provided. 
        # SQL: SELECT * FROM products WHERE id = [product_id] LIMIT 1;

        if result.staff_id != staff_id:
            return {"message": "You do not have authorization to post on behalf of other users."}, 403
    
        if not product_search:
            return {"message": "The product you've entered does not exist."}, 400
        
        db.session.add(result)
        db.session.commit()
                    
        return { "result": result_schema.dump(result),
                "staff_member": f"{usersname}"
                }
                
    except IntegrityError:
        db.session.rollback()
        return {"message": "The product has failed its test, please retest."}, 400
        

@result.put("/<int:id>")
@jwt_required()
def update_result(id):
    current_user_claims = get_jwt()
    user_id = current_user_claims.get('user_id')
    result = db.session.query(Result).filter_by(id=id).first()
    # This searches Results and filters for the result that has the ID provided. 
    # SQL: SELECT * FROM results WHERE id = [id] LIMIT 1;

    if not result:
        return {"message": "There is no result with this id number."}, 400

    if result.staff_id != user_id:
        return {"message": "You are not authorized to update this result."}, 403

    result_fields = result_schema.load(request.json)
    for field in result_fields:
        setattr(result, field, result_fields[field])
    db.session.commit()
    return {"updated result": result_schema.dump(result)}

        
@result.delete("/<int:id>")
@jwt_required()
def delete_result(id):
    current_user_claims = get_jwt()
    role = current_user_claims.get('role')
    result = Result.query.filter_by(id=id).first()
    # This searches Results and filters for the result that has the ID provided. 
    # SQL: SELECT * FROM results WHERE id = [id] LIMIT 1;

    if role != "lab":
        return {"message": "You do not have authorization to delete results."}, 403

    if not result:
        return {"message": "This result does not exist"}, 400

    db.session.delete(result)
    db.session.commit()
    return {"message": "This result has been deleted"} 


@result.get("/product_results/<int:id>")
def get_product_results(id):
    product_results = db.session.query(Result)\
                        .join(User)\
                        .join(Product)\
                        .filter(Result.product_code == id).all()
    
    if not product_results:
        return {"message": "No results found for that product code."}, 400

    result_data = []
    for result in product_results:
        result_dict = productresult_schema.dump(result)
        result_dict['user_name'] = result.user.name
        result_dict['product_name'] = result.product.product_name
        result_data.append(result_dict)
    return result_data      

# This queries all columns of the results table, getting results where the product code is = to id provided, and joins user and product table

# sql: 
# SELECT * FROM results
# JOIN users ON results.user_id = users.id
# JOIN products ON results.product_code = products.id
# WHERE results.product_code = [id];
