from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class TXLog(Base):

    __tablename__ = "tx_log"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session = Column(
        String
    )

    operation = Column(
        String
    )

    inicio = Column(
        DateTime
    )

    fin = Column(
        DateTime
    )

    wait_time = Column(
        Float
    )

    lock_type = Column(
        String
    )

    resolution = Column(
        String
    )