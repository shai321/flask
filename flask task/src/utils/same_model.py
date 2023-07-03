from sqlalchemy import Column, DateTime, String, Boolean
from datetime import datetime

class DBmodel():
    __tablename__ = "samemodel"

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(String())
    is_active = Column(Boolean, default=True)