import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Optional

from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.repository.user import user_repo_plus
from app.routers.dependecies import login_service
from app.schemas.user_create import CreateUserModel
from app.routers.dependecies import register_service
from app.service.login import LoginService
from app.service.register import RegisterService
from app.secure.autificate import get_auth_user
from app.schemas.verify import VerifyCode


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


@router.post("/register")
async def register_users(
    user_service: Annotated[RegisterService, Depends(register_service)],
    data:CreateUserModel
):
    result = await user_service.register(data)


@router.post(
   "/signin/token-username"
)
async def create_token_endpoint(
        users_service: Annotated[LoginService, Depends(login_service)],
        data: OAuth2PasswordRequestForm = Depends()
):
    result = await users_service.login_by_username(data)
    return result

@router.post(
    "/profile"
)
async def profile(
    payload:dict = Depends(get_auth_user)
): 
    return payload
    
@router.post(
    "/send_code"
)
async def send_code(
    user_service: Annotated[RegisterService, Depends(register_service)],
    id:int
):
    result = await user_service.sendcode(id = id)

@router.post(
    "/verify_code"
)
async def verify_code(
    user_service: Annotated[RegisterService, Depends(register_service)],
    data: VerifyCode
):
    result = await user_service.verify_code(data = data)