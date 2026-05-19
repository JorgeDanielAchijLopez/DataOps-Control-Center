from fastapi import FastAPI

from app.database import Base, engine
from app.models.connection import Connection

from app.routes.connection_routes import router as connection_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DataOps Control Center API",
    version="1.0.0"
)

app.include_router(
    connection_router
)


@app.get("/")
def home():

    return {
        "message":
        "DataOps Control Center API funcionando"
    }