import random
import time

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from app.database import SessionLocal
from app.models.tx_log import TXLog


operations = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "SELECT"
]

lock_types = [
    "SHARED",
    "EXCLUSIVE",
    "DEADLOCK",
    "TIMEOUT"
]


def simulate_user_transaction(
    user_id
):

    db = SessionLocal()

    try:

        start = datetime.utcnow()

        wait_time = round(
            random.uniform(
                10,
                900
            ),
            2
        )

        time.sleep(
            wait_time / 1000
        )

        lock_type = random.choices(
            lock_types,
            weights=[
                60,
                25,
                10,
                5
            ],
            k=1
        )[0]

        if lock_type == "DEADLOCK":

            resolution = (
                "Deadlock detectado y sesión finalizada automáticamente"
            )

        elif lock_type == "TIMEOUT":

            resolution = (
                "Transacción cancelada por tiempo de espera"
            )

        else:

            resolution = (
                "Transacción completada correctamente"
            )

        tx = TXLog(

            session =
            f"session_{user_id}",

            operation =
            random.choice(
                operations
            ),

            inicio =
            start,

            fin =
            datetime.utcnow(),

            wait_time =
            wait_time,

            lock_type =
            lock_type,

            resolution =
            resolution
        )

        db.add(
            tx
        )

        db.commit()

    finally:

        db.close()


def run_concurrency_test():

    with ThreadPoolExecutor(
        max_workers=20
    ) as executor:

        for user_id in range(
            1,
            101
        ):

            executor.submit(
                simulate_user_transaction,
                user_id
            )

    print(
        "Prueba de concurrencia ejecutada con 100 usuarios",
        flush=True
    )