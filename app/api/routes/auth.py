
import uuid
from fastapi import APIRouter, HTTPException
from store import get_current_user, reset_current_user, set_current_user
from model.daemon import PrivyDaemon
from service.daemon_service import start_daemons_for_user, start_daemon
from model.user import PrivyUser, PrivyUserCreate, PrivyUserLogin
from store import save_user, get_user_by_name, get_all_users


router = APIRouter()

@router.post("/login")
async def login(payload: PrivyUserLogin):
    # set current user to this
    current_user = get_current_user()
    if current_user is not None:
        raise HTTPException(status_code=401, detail=f"Already logged in as {current_user.username}. Logout before logging in!")
    if len(get_all_users()) < 1:
        raise HTTPException(status_code=404, detail=f"There are currently no accounts registered on this device. Try adding an existing account or creating a new oen")
    user = get_user_by_name(payload.username)
    if user is None:
        raise HTTPException(status_code=404, detail=f"No such user was found! Try adding an existing account or creating a new one!")
    # check credentials
    if payload.password != user.password:
        raise HTTPException(status_code=401, detail=f"Credentials do not match! Verify given password is correct!")
    set_current_user(user)
    return f"Logged in as {user.username}"


@router.post("/register")
def register(payload: PrivyUserCreate):
    # check if username available locally
    if get_user_by_name(payload.username):
        raise HTTPException(status_code=409, detail="Given username is already in use on this device!")
    daemon = PrivyDaemon(id=uuid.uuid4().hex, type="origin", name=f"{payload.username}-origin", repo=uuid.uuid4().hex)
    user = PrivyUser(username=payload.username, password=payload.password, daemons=[daemon])
    
    #start_daemon(daemon)
    return save_user(user)
    

@router.post("/add-account")
def add_account(payload: PrivyUserLogin):
    # check if username available locally
    if get_user_by_name(payload.username):
        raise HTTPException(status_code=409, detail="Given username is already in use on this device!")
    daemon = PrivyDaemon(id=uuid.uuid4().hex, type="remote", name=f"{payload.username}-remote", repo=uuid.uuid4().hex)
    user = PrivyUser(username=payload.username, password=payload.password, daemons=[daemon])
    #start_daemon(daemon)
    return save_user(user)


@router.post("/logout")
async def logout():
    reset_current_user()
    return f"Successfully logged out!"


@router.get("/whoami")
async def whoami():
    """
    Get display name of currently logged in user
    """
    current_user = get_current_user()
    if current_user is None:
        raise HTTPException(status_code=400, detail=f"Not logged in!")
    return current_user.username
