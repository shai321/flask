from src.database import db
from src.user_cohort.model import UserCohort
from src.user.model import User
from src.cohort.model import Cohort
from src.utils.token import token_required
from flask import Blueprint, g, request, jsonify
import threading

user_cohort = Blueprint("user_group", __name__)

def send_background_message(user_id, message):
    for user in user_id:
        print(f"Sending message to user {user}: {message}")

@user_cohort.route("/add_user_group", methods=["POST"])
def add_users():
    add_user = UserCohort(**request.json)
    if UserCohort.query.filter(
        UserCohort.user_id == add_user.user_id, UserCohort.cohort_id == add_user.cohort_id
    ).first():
        return {"message": "user already exist"}
    else:
        db.session.add(add_user)
        db.session.commit()
        return jsonify(
            {
                "id": add_user.id,
                "user_id": add_user.user_id,
                "cohort_id": add_user.cohort_id,
            }
        )

@user_cohort.route("/send_message", methods=["POST"])
def get_user_message():
    cohort_id = request.json.get("cohort_id")
    message = request.json.get("message")

    cohort_users = UserCohort.query.filter(UserCohort.cohort_id == cohort_id).all()
    cohort_detail = Cohort.query.filter(Cohort.id == cohort_id).first()
    user_id = []
    for cohort_user in cohort_users:
        user_id.append(cohort_user.user_id)
        print(f"Sending message to user {cohort_user.user_id}: {message}")
    # thread = threading.Thread(target=send_background_message, args=(user_id, message))
    # thread.start()

    return jsonify({
        "cohort": {
            "cohort_id": cohort_id,
            "cohort_name": cohort_detail.cohort_name
        },
        "user": user_id,
        "message": message

    })

@user_cohort.route("/user_remove", methods=["DELETE"])
@token_required
def remove_user():
    user = User.query.get(g.user_data.id)
    cohort_id = request.json.get("cohort_id")
    if UserCohort.query.filter(UserCohort.user_id == user, UserCohort.cohort_id == cohort_id).first():
        db.session.delete()
        db.session.commit()
        return {"message": "user deleted successfully"}
    else:
        return {"message": "user is not define"}
