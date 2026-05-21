from fastapi import APIRouter
import redis
import json
import time


router = APIRouter(
    prefix="/cache",
    tags=["Cache"]
)


r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)


cache_hits = 0
cache_misses = 0


@router.get("/query/{query_key}")
def cached_query(
    query_key: str
):

    global cache_hits
    global cache_misses

    start = time.time()

    data = r.get(
        query_key
    )

    if data:

        cache_hits += 1

        return {

            "source":
            "CACHE",

            "time_ms":
            round(
                (
                    time.time() - start
                ) * 1000,
                2
            ),

            "data":
            json.loads(
                data
            )
        }

    cache_misses += 1

    time.sleep(
        0.4
    )

    fake_result = {

        "query":
        query_key,

        "rows":
        150
    }

    r.setex(

        query_key,

        60,

        json.dumps(
            fake_result
        )
    )

    return {

        "source":
        "DATABASE",

        "time_ms":
        round(
            (
                time.time() - start
            ) * 1000,
            2
        ),

        "data":
        fake_result
    }


@router.delete(
    "/invalidate/{query_key}"
)
def invalidate_cache(
    query_key: str
):

    r.delete(
        query_key
    )

    return {

        "message":
        "Cache eliminada"
    }


@router.get("/summary")
def cache_summary():

    total = (

        cache_hits +
        cache_misses
    )

    ratio = 0

    if total > 0:

        ratio = round(
            (
                cache_hits /
                total
            ) * 100,
            2
        )

    return {

        "hits":
        cache_hits,

        "misses":
        cache_misses,

        "hit_ratio":
        ratio,

        "ttl":
        "60 segundos"
    }