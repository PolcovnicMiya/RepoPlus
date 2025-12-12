import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Optional

from fastapi.responses import JSONResponse
from app.repository.user import user_repo
from app.routers.dependecies import login_service, register_service
from app.schemas.user_create import CreateUserModel
from app.schemas.register_response import RegisterResponseModel
from app.schemas.login_email import LoginEmailSchema
from app.schemas.profile_response import ProfileResponseModel
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
async def user(user_id: int):
    result = await user_repo.get_one(id=user_id)
    return {"result": result}




@router.post("/all_users")
async def all_users(filt: dict = None):
    if filt:
        log.info(filt)
    result = await user_repo.get_all(filters=filt)
    return {"result": result}


@router.post("/create")
async def create_user(data: CreateUserModel):
    data = data.model_dump()
    result = await user_repo.add_one(data=data)
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
async def delete_user(user_id: int):
    result = await user_repo.delete_one(id=user_id)
    return {"result": result}


@router.post("/register", response_model=RegisterResponseModel)
async def register_users(
    user_service: Annotated[RegisterService, Depends(register_service)],
    data: CreateUserModel
) -> RegisterResponseModel:
    result = await user_service.register(data)
    return result


@router.post("/signin")
async def login(
    users_service: Annotated[LoginService, Depends(login_service)],
    data: LoginEmailSchema
):
    result = await users_service.login_by_email(email=data.email, password=data.password)
    return result


@router.get("/profile", response_model=ProfileResponseModel)
async def profile(
    payload: dict = Depends(get_auth_user)
) -> ProfileResponseModel: 
    return ProfileResponseModel(**payload)
    

@router.post("/send_code")
async def send_code(
    user_service: Annotated[RegisterService, Depends(register_service)],
    id: int
):
    result = await user_service.sendcode(id=id)
    return result


@router.post("/verify_code")
async def verify_code(
    user_service: Annotated[RegisterService, Depends(register_service)],
    data: VerifyCode
):
    result = await user_service.verify_code(data=data)
    return result
