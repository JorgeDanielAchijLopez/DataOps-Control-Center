from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class TXLog(Base):

    __tablename__="tx_log"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    transaction_name=Column(
        String
    )

    status=Column(
        String
    )

    lock_type=Column(
        String
    )

    created_at=Column(
        DateTime,
        default=datetime.utcnow
    )