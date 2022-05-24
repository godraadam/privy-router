from fastapi import APIRouter


from .routes import auth, account, contact

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(account.router, prefix="/account")
router.include_router(contact.router, prefix="/contact")


@router.post("/ping")
def ping():
    return
