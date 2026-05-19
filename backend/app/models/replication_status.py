from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class ReplicationStatus(Base):

    __tablename__ = "replication_status"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    primary_node = Column(
        String
    )

    replica_node = Column(
        String
    )

    replication_lag = Column(
        Float
    )

    status = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )