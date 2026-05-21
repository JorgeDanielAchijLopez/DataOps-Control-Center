from fastapi import APIRouter
from fastapi import HTTPException
from jose import jwt
from datetime import datetime
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

SECRET_KEY = "dataops_secret_key"
ALGORITHM = "HS256"


@router.post("/login")
def login(data: dict):

    username = data.get("username")
    password = data.get("password")

    if username != "admin" or password != "admin123":

        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
