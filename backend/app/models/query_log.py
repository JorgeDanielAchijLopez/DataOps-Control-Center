from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class QueryLog(Base):

    __tablename__ = "query_log"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    query_text = Column(
        String,
        nullable=False
    )

    duration_ms = Column(
        Float,
        nullable=False
    )

    rows_returned = Column(
        Integer,
        default=0
    )

    index_used = Column(
        String,
        nullable=True
    )

    execution_plan = Column(
        String,
        nullable=True
    )

    classification = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )