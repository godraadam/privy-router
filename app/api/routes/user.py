from fastapi import APIRouter
import store

router = APIRouter()

@router.get("/")
def get_all_users():
    return store.get_all_users()