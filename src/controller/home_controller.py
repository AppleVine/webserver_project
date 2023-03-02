from flask import Blueprint


home = Blueprint('home', __name__, url_prefix='/')

@home.get("/")
def homepage():
    return {"message": "Hello World"}