from flask import Blueprint, request, jsonify
from model.user import User
from model.product import Product
from model.result import Result
from schema.users_schema import user_schema, users_schema
from schema.results_schema import userresults_schema
from app import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from app import app
from function import *
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import exc



user = Blueprint('user', __name__, url_prefix='/users')


@app.route("/register", methods=["POST"])
def create_user():
    try:
        user_fields = user_schema.load(request.json)
        user = User(**user_fields)
        token = create_access_token(identity=user_fields["username"])
        db.session.add(user)
        db.session.commit()
        return { "user": user_schema.dump(user), "token": token}
    except IntegrityError as e:
        db.session.rollback()
        if 'unique constraint' in str(e).lower():
            return {"message": "You already have an account, please login instead."}, 400
        elif 'check constraint' in str(e).lower():
            return {"message": "Your login details do not match the constraints. Your email must be 5-30 characters long, username 5-20, password 8-30, name 2-30 and role must be 3-20."}, 400
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return {"message": "An error occurred while creating your account."}, 500

            

@app.route("/login", methods=["POST"])
def login():
    user_fields = user_schema.load(request.json)
    username = user_fields["username"],
    password = user_fields["password"],
    user = db.one_or_404(db.select(User).filter_by(username=username).filter_by(password=password))
    if user:
        token = create_access_token(identity=user_fields["username"])
        return {"username": user_schema.dump(user), "token": token}
    else:
        return {"message": "Username or Password is incorrect"}
    

@user.get("/")
@check_access(role=["lab"])
def get_users():
    users = User.query.all()
    return users_schema.dump(users)


@user.get("/<int:id>")
def get_user(id):
    if check_id(id) == True or check_access_boolean(role=["lab"]) == True:
        user = User.query.get(id)
        return user_schema.dump(user)
    else:
        raise NoAuthorizationError("You are not able to view this persons details.")



    
@user.get("/user_results/<int:id>")
def get_user_results(id):
     
    # user_results = db.session.query(
    #     User, Product, Result).filter(User.id == Result.staff_id).filter(Result.product_code == Product.id).filter(Result.staff_id == id).all()
    
    # return jsonify(user_results)
    # TypeError: Object of type Row is not JSON serializable

    # return {"user results": user_results.dump(id)}
    # AttributeError: 'list' object has no attribute 'dump'

    # return results_schema.dump(user_results)
    # No error, but returned nothing. 

    # --------------------

    # user_results = db.select(Result).filter_by(Result.staff_id == id)
    # return result_schema.dump(user_results)
    # TypeError: filter_by() takes 1 positional argument but 2 were given

    # ------------------

    # results = Result.query.get(Result.staff_id == id)
    # return results_schema.dump(results)
    # TypeError: Boolean value of this clause is not defined

    # -----------------
    

    user_results = db.session.query(Result).join(User).join(Product).filter(Result.staff_id == id).all()

    return userresults_schema.dump(user_results)
    
    
    # return staff_results_schema.dump(user_results)
    # Works to return in the results_schema. Need to make it show staff name instead of ID and show product name. 

    # -----------------
    
    # user_results = db.session.query(Result).join(User).join(Product).filter(Result.staff_id == id).all()

    # return {
    #     "result_id": user_results.Result.id,
    #     "staff_name": user_results.User.name,
    # }


    # -----------------

    # query = db.session.query(User.name, Product.id, Result.id).\
    # join(Result, User.id == Result.staff_id).\
    # join(Product, Product.id == Result.product_code).\
    # filter(Result.staff_id == id)

    # return staff_results_schema.dump(query)
    # return query

    # -----------------

    # query = db.session.query(Result).\
    # join(User, User.id == Result.staff_id).\
    # join(Product, Product.id == Result.product_code).\
    # filter(Result.staff_id == id)


    
    # return staff_results_schema.dump(staff)


    # -----------------
    # user_results = db.session.query(Result).join(User).join(Product).filter(Result.staff_id == id).all()
    # print(user_results.staff_id)

    # -----------------

    #     results = db.session.query(Result).filter(Result.staff_id == id).all()
    #     user = db.session.query(User).filter(User.id == results.staff_id)

    #     return {
    #         "result_id": results.id,
    #         "staff_id": results.staff_id,
    #         "staff_name": user.name
    #     }


    # fields = ('id', 'staff_name', 'staff_id', 'product_code', 'product_code', 'specific_gravity', 'pH', 'reserve_alkalinity', 'water_content', 'test_time_date')

    # -----------------

