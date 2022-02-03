from fastapi import APIRouter, HTTPException
from model.user import PrivyUser, PrivyUserCreate, PrivyUserLogin
from service import account_service
import store

router = APIRouter()


@router.post(
    "/add",
    response_model=PrivyUser,
    response_model_exclude={"password"},
    response_model_exclude_none=True,
)
def add_account(payload: PrivyUserLogin):
    # check if username available locally
    if store.get_user_by_name(payload.username):
        raise HTTPException(status_code=409)
    return account_service.add_account(payload)


@router.post(
    "/create",
    response_model=PrivyUser,
    response_model_exclude={"password"},
    response_model_exclude_none=True,
)
def register(payload: PrivyUserCreate):
    # check if username available locally
    if store.get_user_by_name(payload.username):
        raise HTTPException(status_code=409)
    return account_service.create_account(payload)


@router.delete("/remove/{username:str}")
def remove_account(username: str):
    user = store.get_user_by_name(username)
    if user is None:
        raise HTTPException(status_code=404)
    account_service.remove_account(user)
    return user.username
