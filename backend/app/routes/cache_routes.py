from fastapi import APIRouter
import random

router = APIRouter(
    prefix="/cache",
    tags=["Cache"]
)

cache_hits = 0
cache_misses = 0


@router.get("/query/{query_key}")
def cache_query(
    query_key: str
):

    global cache_hits
    global cache_misses

    hit = random.choice(
        [True, False]
    )

    if hit:

        cache_hits += 1

        return {
            "status":
            "CACHE HIT",

            "query":
            query_key
        }

    cache_misses += 1

    return {

        "status":
        "CACHE MISS",

        "query":
        query_key
    }


@router.get("/summary")
def cache_summary():

    total = (
        cache_hits +
        cache_misses
    )

    ratio = (

        round(
            (
                cache_hits /
                total
            ) * 100,
            2
        )

        if total > 0
        else 0
    )

    return {

        "hits":
        cache_hits,

        "misses":
        cache_misses,

        "hit_ratio":
        ratio
    }