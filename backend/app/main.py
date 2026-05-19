from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import Base
from app.database import engine

from app.models.connection import Connection
from app.models.db_metric import DBMetric

from app.routes.connection_routes import router as connection_router
from app.routes.metric_routes import router as metric_router

from app.services.health_service import run_health_check

Base.metadata.create_all(
    bind=engine
)

app=FastAPI(
    title="DataOps Control Center API",
    version="1.0.0"
)

app.include_router(
    connection_router
)

app.include_router(
    metric_router
)

scheduler=BackgroundScheduler()

scheduler.add_job(
    run_health_check,
    "interval",
    seconds=10
)

scheduler.start()


@app.get("/")
def home():

    return{
        "message":
        "DataOps Control Center API funcionando"
    }