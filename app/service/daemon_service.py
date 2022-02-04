from service.docker_service import (
    create_privyd_container,
    exists_privyd_container,
    remove_privyd_container,
    start_privyd_container,
)
import util
from model.daemon import PrivyDaemon
import logging

from model.user import PrivyUser


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def start_daemon(daemon: PrivyDaemon, user: PrivyUser):
    logger.info(f"Starting daemon {daemon.name} for user {user.username}")

    # derive seed
    seed = util.derive_seed(user.username, user.password)    

    # if container doesn't exist create it
    if not exists_privyd_container(daemon.name):
        port = util.get_available_port()
        daemon.port = port
        create_privyd_container(daemon, seed, port)

    # start the container
    start_privyd_container(daemon.name)


def start_daemons_for_user(user: PrivyUser):
    logger.info(f"Starting daemons for {user.username}")
    for daemon in user.daemons:
        start_daemon(daemon, user)


def remove_daemons_for_user(user: PrivyUser):
    logger.info(f"Removing daemons for {user.username}")
    for daemon in user.daemons:
        remove_privyd_container(daemon.name)
