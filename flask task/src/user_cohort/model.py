from src.database import db
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from src.user.model import User
from src.cohort.model import Cohort
import uuid
from src.utils.same_model import DBmodel

class UserCohort(DBmodel, db.Model):
    __tablename__ = "usercohort"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    cohort_id = Column(ForeignKey(Cohort.id))
    user_id = Column(ForeignKey(User.id))

    