import random
import time

from app.database import SessionLocal
from app.models.query_log import QueryLog


def simulate_query():

    db = SessionLocal()

    try:

        fake_queries = [
            "SELECT * FROM users",
            "SELECT * FROM orders",
            "SELECT * FROM products",
            "UPDATE users SET active = true",
            "DELETE FROM logs"
        ]

        query = random.choice(
            fake_queries
        )

        start = time.time()

        simulated_delay = random.uniform(
            0.05,
            3
        )

        time.sleep(
            simulated_delay
        )

        duration_ms = (
            time.time() - start
        ) * 1000

        if duration_ms < 100:
            classification = "FAST"

        elif duration_ms < 500:
            classification = "MEDIUM"

        elif duration_ms < 2000:
            classification = "SLOW"

        else:
            classification = "CRITICAL"

        query_log = QueryLog(
            query_text=query,
            duration_ms=round(duration_ms, 2),
            rows_returned=random.randint(1, 1000),
            index_used="idx_users" if random.random() > 0.5 else None,
            execution_plan="Sequential Scan",
            classification=classification
        )

        db.add(
            query_log
        )

        db.commit()

        print(
            f"Query registrada: {classification} - {duration_ms:.2f} ms",
            flush=True
        )

    finally:

        db.close()