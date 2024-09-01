import logging
from fastapi import APIRouter
from app.MyRepository.user import user_repo
from app.schemas.user import CreateUserModel

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
log = logging.getLogger("__name__")


@router.get("/")
async def user(user_id: int):
    result = await user_repo.get_one(id=user_id)
    return {"result": result}

@router.post("/users")
async def user_all(filters:dict = None):
    result = await user_repo.get_all(filters=filters)
    return {"result": result}

@router.post("/create")
async def create_user(data: CreateUserModel):
    data = data.model_dump()
    result = await user_repo.add_one(data=data)
    return {"result": result}


@router.post("/all_users")
async def all_users(filt: dict = None):
    if filt:
        log.info(filt)
    result = await user_repo.get_all(filters=filt)
    return {"result": result}


@router.put("/edit")
async def edit_user(filt: dict, data: CreateUserModel):
    data = data.model_dump()
    result = await user_repo.edit_one(filters=filt, data=data)
    return {"result": result}


@router.put("/edit_some")
async def edit_some_user(filt: dict, data: CreateUserModel):
    data = data.model_dump()
    result = await user_repo.edit_some(filters=filt, data=data)
    return {"result": result}

@router.delete("/delete")
async def delete_user( user_id :int):
    result = await user_repo.delete_one(id = user_id)
    return {"result": result}

