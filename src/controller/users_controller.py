from flask import Blueprint, request
from model.user import User
from schema.users_schema import user_schema, users_schema
from app import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from app import app


user = Blueprint('user', __name__, url_prefix='/users')

@user.get("/")
def get_users():
    users = User.query.all()
    return users_schema.dump(users)


@user.get("/<int:id>")
def get_user(id):
    user = User.query.get(id)
    if not user:
        return {"message": "There is no user with this id."}
    return user_schema.dump(user)
## Change to try, except: If wrong access token return incorrect credentials, if no user, no user found etc...
##############################



@app.route("/register", methods=["POST"])
def create_user():
    # try:
        user_fields = user_schema.load(request.json)
        user = User(**user_fields)
        token = create_access_token(identity=user_fields["username"])
        db.session.add(user)
        db.session.commit()
        return { "user": user_schema.dump(user), "token": token}
        
    # except:
    #     return {"message": "Your information is incorrect"}
    

@app.route("/login", methods=["POST"])
def login():
    user_fields = user_schema.load(request.json)
    username = user_fields["username"],
    password = user_fields["password"],
    user = db.one_or_404(db.select(User).filter_by(username=username).filter_by(password=password))
    user = db.session.execute(db.select(User).filter_by(username=username).filter_by(password=password))
    if user:
        token = create_access_token(identity=username)
        return {"username": user_schema.dump(user), "token": token}
    else:
        return {"message": "Username or Password is incorrect"}