from src.database import db
from flask import request, jsonify, Blueprint, abort, g
from flask_api import status
from src.user.model import User
from src.cohort.model import Cohort
from src.utils.error_handel import TaskException

cohort = Blueprint("cohort", __name__)

@cohort.route("/create_cohort", methods=["POST"])
def cohort_create():
    cohort_detail = Cohort(**request.json)
    if Cohort.query.filter(Cohort.cohort_name == cohort_detail.cohort_name).first():
        raise TaskException(
            message="Cohort Name Is Already Exist", status_code=status.HTTP_406_NOT_ACCEPTABLE
        )

    db.session.add(cohort_detail)
    db.session.commit()

    return {"message": "Cohort Successfully Created"}
