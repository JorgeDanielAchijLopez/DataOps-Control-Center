from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class DBMetric(Base):

    __tablename__="db_metrics"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    connection_id=Column(
        Integer,
        ForeignKey(
            "connections.id"
        )
    )

    cpu=Column(
        Float
    )

    memory=Column(
        Float
    )

    connections=Column(
        Integer
    )

    locks=Column(
        Integer
    )

    deadlocks=Column(
        Integer
    )

    disk_usage=Column(
        Float
    )

    capture_time=Column(
        DateTime,
        default=datetime.utcnow
    )