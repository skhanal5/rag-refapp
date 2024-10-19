from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def get_health():
    return {"hello": "world"}


@router.get("/database")
async def get_database_health():
    return {"hello": "world"}
