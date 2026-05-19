from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.connection import Connection

router = APIRouter(
    prefix="/connections",
    tags=["Connections"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_connection(
    data: dict,
    db: Session = Depends(get_db)
):

    connection = Connection(
        name=data["name"],
        engine=data["engine"],
        host=data["host"],
        port=data["port"],
        username=data["username"],
        password=data["password"]
    )

    db.add(connection)

    db.commit()

    return {
        "message":
        "Conexión registrada correctamente"
    }


@router.get("/")
def get_connections(
    db: Session = Depends(get_db)
):

    return db.query(
        Connection
    ).all()