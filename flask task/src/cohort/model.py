from src.database import db
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.user.model import User
from src.utils.same_model import DBmodel

class Cohort(DBmodel, db.Model):
    __tablename__ = "cohort"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    cohort_name = Column(String())
    cohort_work = Column(String())
    