from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class AlertLog(Base):

    __tablename__="alert_log"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    db_id=Column(
        Integer
    )

    severity=Column(
        String
    )

    condition=Column(
        String
    )

    message=Column(
        String
    )

    status=Column(
        String,
        default="OPEN"
    )

    created_at=Column(
        DateTime,
        default=datetime.utcnow
    )