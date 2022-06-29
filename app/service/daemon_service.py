import os
import subprocess
import requests
from app import util
from app.model.daemon import PrivyDaemon
import logging
from app.config import settings
from app.model.user import PrivyUser


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def start_daemon(daemon: PrivyDaemon, user: PrivyUser):
    logger.info(f"Starting daemon {daemon.name} for user {user.username}")
    
    seed = util.derive_seed(user.mnemonic)

    os.environ["PORT"] = f"{daemon.port}"
    os.environ["SEED"] = seed
    os.environ["USERNAME"] = user.username
    os.environ["REPO"] = daemon.repo
    os.environ["NODE_TYPE"] = daemon.type

    subprocess.Popen(["node", settings.PATH_TO_DAEMON])

def start_daemons_for_user(user: PrivyUser):
    logger.info(f"Starting daemons for {user.username}")
    for daemon in user.daemons:
        start_daemon(daemon, user)
