from src.database import db
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.utils.same_model import DBmodel

class User(DBmodel, db.Model):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    email_id = Column(String(), unique=True)
    password = Column(String())
