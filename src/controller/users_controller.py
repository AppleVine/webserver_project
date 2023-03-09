from flask import Blueprint, request, jsonify
from model.user import User
from model.product import Product
from model.result import Result
from schema.users_schema import user_schema, users_schema
from schema.results_schema import userresults_schema
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager, get_jwt
from app import app
from function import *
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import exc



user = Blueprint('user', __name__, url_prefix='/users')


@app.post("/register")
def create_user():
    try:
        user_fields = user_schema.load(request.json)
        user = User(**user_fields)
        
        db.session.add(user)
        db.session.commit()

        user_id = user.id
        token = create_access_token(identity=user_fields["username"], additional_claims={"user_id": user_id, "role": user_fields["role"]})

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

            

@app.post("/login")
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
@jwt_required()
def get_users():
    current_user_claims = get_jwt()
    user_role = current_user_claims.get('role')
    if user_role != "lab":
        return {"message": "You are not authorized to view all users information."}, 403
    else:
        users = User.query.all()
        return users_schema.dump(users)



@user.get("/<int:id>")
def get_user(id):
    if check_id(id) == True or check_access_boolean(role=["lab"]) == True:
        user = User.query.get(id)
        return user_schema.dump(user)
    else:
        raise NoAuthorizationError("You are not able to view this persons details.")


@user.put("/<int:id>")
@jwt_required()
def update_user(id):
    current_user_claims = get_jwt()
    user_id = current_user_claims.get('user_id')
    if user_id != id:
        return {"message": "You are not authorized to update this user's information",
                "current_user_id": f'{user_id}',
                "id": f'{id}'
                }, 403
    else:
        user_fields = user_schema.load(request.json)
        user = User.query.filter_by(id=id).first()
        if user is not None:
            for field in user_fields:
                setattr(user, field, user_fields[field])
            db.session.commit()
            token = create_access_token(identity=user_fields["username"], additional_claims={"user_id": user_id})
            return { "user": user_schema.dump(user), "token": token}
    return {"message": "User not found"}, 404





# @user.put("/<int:id>")
# @jwt_required()
# def update_user(id):
#     current_user_id = get_jwt_identity()
#     if current_user_id != id:
#         return {"message": "You are not authorized to update this user's information"}, 403

#     if check_id(id) == True:
#         user_fields = user_schema.load(request.json)
#         user = User.query.filter_by(id=id).first()
#         if user is not None:
#             for field in user_fields:
#                 setattr(user, field, user_fields[field])
#             db.session.commit()
#             token = create_access_token(identity=user_fields["username"])
#             return { "user": user_schema.dump(user), "token": token}
#     return {"message": "User not found"}, 404


# @user.put("/<int:id>")
# @jwt_required()
# def update_user(id):
#     current_user_id = get_jwt_identity()
#     if current_user_id != id:
#         return {"message": "You are not authorized to update this user's information"}, 403
#     user = User.query.filter_by(id = id).first()
#     if user:
#         user_fields = user_schema.load(request.json)
#         for field in user_fields:
#             setattr(user, field, user_fields[field])
#         db.session.commit()
#         token = create_access_token(identity=user.username)
#         return { "user": user_schema.dump(user), "token": token}



        # except IntegrityError as e:
        #     db.session.rollback()
        #     if 'unique constraint' in str(e).lower():
        #         return {"message": "You already have an account, please login instead."}, 400
        #     elif 'check constraint' in str(e).lower():
        #         return {"message": "Your login details do not match the constraints. Your email must be 5-30 characters long, username 5-20, password 8-30, name 2-30 and role must be 3-20."}, 400
        # except SQLAlchemyError as e:
        #     db.session.rollback()
        #     print(e)
        #     return {"message": "An error occurred while creating your account."}, 500



    
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

