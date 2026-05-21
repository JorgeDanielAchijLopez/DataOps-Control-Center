from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class SnapshotLog(Base):

    __tablename__ = "snapshot_log"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    description = Column(String)

    status = Column(String)

    rpo_minutes = Column(Float)

    rto_minutes = Column(Float)

    sla_status = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)