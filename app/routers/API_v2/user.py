import logging
from fastapi import APIRouter
from app.MyRepository.user import user_repo_plus
from app.schemas.user import CreateUserModel

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
log = logging.getLogger("__name__")


@router.get("/")
async def user(user_id: int, test : bool = False):
    result = await user_repo_plus.get_one(id=user_id, test=test)
    return {"result": result}


@router.post("/all_users")
async def all_users(filt: dict = None,test:bool = False ):
    if filt:
        log.info(filt)
    result = await user_repo_plus.get_all(filters=filt, test=test)
    return {"result": result}


@router.post("/create")
async def create_user( data: CreateUserModel, test:bool = False ):
    data = data.model_dump()
    result = await user_repo_plus.add_one(data=data, test=test)
    return {"result": result}


@router.put("/edit")
async def edit_user( id:int , data: CreateUserModel,test:bool = False):
    data = data.model_dump()
    result = await user_repo_plus.edit_one(test=test,id = id, data=data)
    return {"result": result}


@router.put("/edit_some")
async def edit_some_user(filt: dict, data: CreateUserModel,test:bool = False):
    data = data.model_dump()
    result = await user_repo_plus.edit_some(filters=filt, data=data, test=test)
    return {"result": result}

@router.delete("/delete")
async def delete_user(user_id :int, test:bool = False):
    result = await user_repo_plus.delete_one(id = user_id, test=test)
    return {"result": result}

