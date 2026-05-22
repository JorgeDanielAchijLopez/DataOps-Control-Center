from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class RecoveryLog(Base):

    __tablename__ = "recovery_log"

    id = Column(Integer, primary_key=True, index=True)

    event_type = Column(String)

    affected_table = Column(String)

    status = Column(String)

    rpo_minutes = Column(Float)

    rto_seconds = Column(Float)

    message = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)