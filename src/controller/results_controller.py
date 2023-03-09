from flask import Blueprint, request
from model.user import User
from model.product import Product
from model.result import Result
from schema.users_schema import user_schema, users_schema
from schema.results_schema import results_schema
from app import db
from flask_jwt_extended import create_access_token, jwt_required,  get_jwt


result = Blueprint('result', __name__, url_prefix='/results')


@result.get("/")
def get_results():
    results = Result.query.all()
    return results_schema.dump(results)


@user.get("/<int:id>")
@jwt_required(optional=True)
def get_user(id):
    current_user_claims = get_jwt()
    if current_user_claims.get('user_id') == id or current_user_claims.get('role') == "lab":
        user = User.query.get(id)
        return user_schema.dump(user)
    else:
        return {"message": "You are not authorized to view this users information."}, 403


@user.get("/user_results/<int:id>")
def get_user_results(id):
    user_results = db.session.query(Result).join(User).join(Product).filter(Result.staff_id == id).all()
    return userresults_schema.dump(user_results)


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
        if user:
            for field in user_fields:
                setattr(user, field, user_fields[field])
            db.session.commit()
            token = create_access_token(identity=user_fields["username"], additional_claims={"user_id": user_id, "role": user_fields["role"]})
            return { "user": user_schema.dump(user), "token": token}
    return {"message": "User not found"}, 404


# @user.delete("/<int:id>")
# @jwt_required()
# def delete_user(id):
#     current_user_claims = get_jwt()
#     if current_user_claims.get('user_id') == id or current_user_claims.get('role') == "lab":
#         user = User.query.filter_by(id=id).first()
#         if user:
#             db.session.delete(user)
#             db.session.commit()
#             return {"message": "this user has been deleted."}
#         else:
#             return {"message": "this user does not exist."}
#  REALIZED I WOULD NEED TO MAKE DELETE CASCADE RESULTS AND WOULD BE A BREACH OF DATA INTEGRITY. 


