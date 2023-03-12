from flask import Blueprint, request
from model.result import Result
from schema.results_schema import results_schema, result_schema
from app import db
from flask_jwt_extended import jwt_required,  get_jwt


result = Blueprint('result', __name__, url_prefix='/results')


@result.get("/")
def get_results():
    results = Result.query.all()
    return results_schema.dump(results)


@result.get("/<int:id>")
def get_result(id):
    result = Result.query.get(id)
    if result:
        return result_schema.dump(result)
    else:
        return {"message": "This result does not exist."}, 400


@result.post("/")
@jwt_required()
def create_result():
    current_user_claims = get_jwt()
    user_role = current_user_claims.get('role')
    staff_id = current_user_claims.get('user_id')
    usersname = current_user_claims.get('name')
    if user_role != "lab":
        return {"message": "You are not authorized to view all users information."}, 403
    else:
        result_fields = result_schema.load(request.json)
        result = Result(**result_fields)
        
        if result.staff_id != staff_id:
            return {"message": "You do not have authorization to post on behalf of other users."}, 403

        else:
            db.session.add(result)
            db.session.commit()
            
            return { "result": result_schema.dump(result),
                    "staff_member": f"{usersname}"
                    }


@result.put("/<int:id>")
@jwt_required()
def update_result(id):
    current_user_claims = get_jwt()
    user_id = current_user_claims.get('user_id')   
    result = db.session.query(Result).filter_by(id=id).first()
    if result:
        if result.staff_id == user_id:
            result_fields = result_schema.load(request.json)
            for field in result_fields:
                setattr(result, field, result_fields[field])
            db.session.commit()
            return {"updated result": result_schema.dump(result)}
        else:
            return {"message": "You are not authorized to update this result."}, 403
    else:
        return {"message": "There is no result with this id number."}, 400
        

@result.delete("/<int:id>")
@jwt_required()
def delete_result(id):
    current_user_claims = get_jwt()
    role = current_user_claims.get('role')
    result = Result.query.filter_by(id=id).first()
    if role == "lab":
        if result:
            db.session.delete(result)
            db.session.commit()
            return {"message": "This result has been deleted"}
        else:
            return {"message": "This result does not exist"}, 400
    else:
        return {"message": "You do not have authorization to delete results."}, 403
