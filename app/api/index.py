from fastapi import APIRouter


from .routes import auth, account, contact, message

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(account.router, prefix="/account")
router.include_router(contact.router, prefix="/contact")
router.include_router(message.router, prefix="/message")


@router.post("/ping")
def ping():
    return "Privy Router is running..."
