from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import Base
from app.database import engine

from app.models.connection import Connection
from app.models.db_metric import DBMetric
from app.models.query_log import QueryLog
from app.models.tx_log import TXLog
from app.models.backup_history import BackupHistory
from app.models.alert_log import AlertLog
from app.models.replication_status import ReplicationStatus
from app.models.snapshot_log import SnapshotLog

from app.routes.connection_routes import router as connection_router
from app.routes.metric_routes import router as metric_router
from app.routes.query_routes import router as query_router
from app.routes.transaction_routes import router as transaction_router
from app.routes.backup_routes import router as backup_router
from app.routes.alert_routes import router as alert_router
from app.routes.replication_routes import router as replication_router
from app.routes.cache_routes import router as cache_router
from app.routes.snapshot_routes import router as snapshot_router
from app.routes.auth_routes import router as auth_router

from app.services.health_service import run_health_check
from app.services.query_service import simulate_query
from app.services.concurrency_service import run_concurrency_test
from app.services.alert_service import run_alert_engine
from app.services.replication_service import monitor_replication
from app.services.snapshot_service import create_default_snapshots

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DataOps Control Center API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(connection_router)
app.include_router(metric_router)
app.include_router(query_router)
app.include_router(transaction_router)
app.include_router(backup_router)
app.include_router(alert_router)
app.include_router(replication_router)
app.include_router(cache_router)
app.include_router(snapshot_router)

scheduler = BackgroundScheduler()

scheduler.add_job(run_health_check,"interval",seconds=10)
scheduler.add_job(simulate_query,"interval",seconds=15)
scheduler.add_job(run_concurrency_test,"interval",seconds=30)
scheduler.add_job(run_alert_engine,"interval",seconds=20)
scheduler.add_job(monitor_replication,"interval",seconds=25)

scheduler.start()

create_default_snapshots()


@app.get("/")
def home():

    return {
        "message":"DataOps Control Center API funcionando"
    }