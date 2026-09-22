from fastapi import APIRouter


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)


@router.get("")
def metrics():
    return {
        "status": "ok",
        "message": "Metrics endpoint is working",
    }