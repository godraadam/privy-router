from fastapi import APIRouter


from .routes import auth, account

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(account.router, prefix="/account")

@router.post("/ping")
def ping():
    return