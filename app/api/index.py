from sys import prefix
from fastapi import APIRouter


from .routes import auth, user

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(user.router, prefix="/user")