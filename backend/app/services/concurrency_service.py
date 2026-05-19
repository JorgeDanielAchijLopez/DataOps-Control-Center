import random

from app.database import SessionLocal
from app.models.tx_log import TXLog


def run_concurrency_test():

    db=SessionLocal()

    try:

        transaction=TXLog(

            transaction_name=
            f"TX_{random.randint(1000,9999)}",

            status=random.choice(
                [
                    "SUCCESS",
                    "WAITING",
                    "DEADLOCK"
                ]
            ),

            lock_type=random.choice(
                [
                    "ROW LOCK",
                    "TABLE LOCK",
                    "PAGE LOCK"
                ]
            )
        )

        db.add(
            transaction
        )

        db.commit()

        print(
            "Concurrencia ejecutada",
            flush=True
        )

    finally:

        db.close()