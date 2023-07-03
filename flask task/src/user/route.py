from src.database import db
from flask import request, jsonify, Blueprint, abort, g
from flask_api import status
from src.user.model import User
from src.utils.error_handel import TaskException
from src.utils.serializer import user_serializer, all_user_serializer
from src.utils.token import create_access_token, token_required
from werkzeug.security import check_password_hash, generate_password_hash

user = Blueprint("user", __name__)


@user.route("/sign_up", methods=["POST"])
def create_user():
    user = User(**request.json)
    if User.query.filter(User.email_id == user.email_id).first():
        # return "User email id already exist", 400
        raise TaskException(
           message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )
    user.password = generate_password_hash(user.password)
    db.session.add(user)
    db.session.commit()
    return jsonify(
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email_id": user.email_id,
        }
    )


@user.route("/sign_in", methods=["POST"])
def check_valid_user():
    email_id = request.json.get("email_id")
    password = request.json.get("password")
    
    user = User.query.filter(
        User.email_id == email_id
    ).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(
            subject={
                "id": str(user.id),
                "email_id": user.email_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )
        return {"access token": access_token}

    else:
        return "Wrong email and password"
    
@user.route("/get/<id>", methods=["GET"])
def get_user(id):
    user = User.query.filter(User.id == id).first()
    if not user:
        raise TaskException(
            "ID not valid", status_code=404
        )
        # abort(400, description="ID not valid")
    return jsonify(
        user_serializer(user)
    )

@user.route("/get_all", methods=["GET"])
def get_all_user():
    all_user = User.query.all()
    return jsonify(all_user_serializer(all_user))

@user.route("/update/", methods=["PUT"])
@token_required
def update():
    # user = User.query.filter(User.id == id).first()
    user = User.query.get(g.user_data.id)

    if 'first_name' in request.json:
        user.first_name = request.json['first_name']
    if 'last_name' in request.json:
        user.last_name = request.json['last_name']
    if 'email_id' in request.json:
        user.email_id = request.json['email_id']
 
    db.session.commit()
    return jsonify({'message': f'{user.id} updated successfully'})

@user.route("/delete", methods=["DELETE"])
@token_required
def delete():
    user = User.query.get(g.user_data.id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'{user.id} deleted successfully'})

# @user.route("/group_of_user", methods=["POST"])
# def group_of_user():

