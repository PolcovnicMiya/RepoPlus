import logging
from fastapi import APIRouter
from app.MyRepository.user import user_repo
from app.schemas.ReadORM.read_user import ReadUSerModel

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
log = logging.getLogger("__name__")


@router.get("/")
async def user(user_id: int):
    result = await user_repo.get_one(id=user_id)
    return {"result": result}


@router.post("/create")
async def create(body: ReadUSerModel):
    body = body.model_dump()
    result = await user_repo.add_one(body=body)
    return {"result": result}


@router.post("/all_users")
async def all_users(filter: dict = None):
    result = await user_repo.get_all(filter=filter)
    return {"result": result}
