from flask import Blueprint, request
from model.user import User
from model.product import Product
from model.result import Result
from schema.users_schema import user_schema, users_schema
from schema.results_schema import userresult_schema, userresults_schema
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from app import app
from sqlalchemy.exc import IntegrityError



user = Blueprint('user', __name__, url_prefix='/users')


@app.post("/register")
def create_user():
    try:
        user_fields = user_schema.load(request.json)
        user = User(**user_fields)
        
        db.session.add(user)
        db.session.commit()

        user_id = user.id
        
        token = create_access_token(identity=user_fields["username"], additional_claims={"user_id": user_id, "role": user_fields["role"], "name": user_fields["name"]})

        return { "user": user_schema.dump(user), "token": token}
    except IntegrityError as e:
        db.session.rollback()
        if 'unique constraint' in str(e).lower():
            return {"message": "You already have an account, please login instead."}, 400
        elif 'check constraint' in str(e).lower():
            return {"message": "Your login details do not match the constraints. Your email must be 5-30 characters long, username 5-20, password 8-30, name 2-30 and role must be 3-20."}, 400


            
@app.post("/login")
def login():
    user_fields = user_schema.load(request.json)
    username = user_fields["username"],
    password = user_fields["password"],
    # This query can only return one user or 404 error, and selects a User where the username and password that are submitted are the same in the table.
    # This is the code in SQL: SELECT * FROM users WHERE username = <username> AND password = <password>;
    user = db.one_or_404(db.select(User).filter_by(username=username).filter_by(password=password))
    if user:
        user_id = user.id
        token = create_access_token(identity=user_fields["username"], additional_claims={"user_id": user_id, "role": user.role, "name": user.name})
        return {"username": user_schema.dump(user), "token": token}
    else:
        return {"message": "Username or Password is incorrect"}, 400
    

@user.get("/")
@jwt_required()
def get_users():
    current_user_claims = get_jwt()
    user_role = current_user_claims.get('role')
    if user_role != "lab":
        return {"message": "You are not authorized to view all users information."}, 403
    else:
        # This query selects all from the user table. In SQL: SELECT * FROM users;
        users = User.query.all()
        return users_schema.dump(users)


@user.get("/<int:id>")
@jwt_required(optional=True)
def get_user(id):
    current_user_claims = get_jwt()
    # This query selects a specific record from the users table, based off of the users id.
    # In SQL: SELECT * FROM users WHERE id = [id];
    user = User.query.get(id)
    if current_user_claims.get('user_id') == id or current_user_claims.get('role') == "lab":
        if user:
            return user_schema.dump(user)
        else:
            return {"message": "No results found for this user id."}, 400
    else:
        return {"message": "You are not authorized to view this users information."}, 403


@user.get("/user_results/<int:id>")
def get_user_results(id):
    user_results = db.session.query(Result)\
                        .join(User)\
                        .join(Product)\
                        .filter(Result.staff_id == id).all()
    if user_results:
        userresult_data = []
        for result in user_results:
            result_dict = userresult_schema.dump(result)
            result_dict['user_name'] = result.user.name
            result_dict['product_name'] = result.product.product_name
            userresult_data.append(result_dict)
        return userresult_data
    else:
        return {"message": "No results found for that user id."}, 400
# This query is a little more complex; it's selecting all the results, where the result's staff id is the same as the id endpoint, then joining the users table with staff_id from results = id from users.
# Then it adds the user's name from that user table. Similarly, it can choose the product based off the product_code (results), as it's joined by id (products), and able to get that product name. The SQL is below:

# SELECT results.*, users.name AS user_name, products.product_name AS product_name 
# FROM results
# JOIN users ON results.user_id = users.id
# JOIN products ON results.product_id = products.id
# WHERE results.staff_id = [id];



@user.put("/<int:id>")
@jwt_required()
def update_user(id):
    current_user_claims = get_jwt()
    user_id = current_user_claims.get('user_id')
    if user_id != id:
        return {"message": "You are not authorized to update this user's information"}, 403
    else:
        user_fields = user_schema.load(request.json)
        user = User.query.filter_by(id=id).first()
        if user:
            for field in user_fields:
                setattr(user, field, user_fields[field])
            db.session.commit()
            token = create_access_token(identity=user_fields["username"], additional_claims={"user_id": user_id, "role": user_fields["role"]})
            return { "user": user_schema.dump(user), "token": token}
    return {"message": "User not found"}, 404

# This selects columns all from the user table where the id of the user matches the id provided, limited to the first option. 
# SQL: SELECT * FROM users WHERE id = [id] LIMIT 1;