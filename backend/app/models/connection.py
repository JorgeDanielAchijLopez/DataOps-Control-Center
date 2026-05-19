from sqlalchemy import Column, Integer, String
from app.database import Base


class Connection(Base):
    __tablename__ = "connections"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    engine = Column(
        String,
        nullable=False
    )

    host = Column(
        String,
        nullable=False
    )

    port = Column(
        String,
        nullable=False
    )

    username = Column(
        String,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )