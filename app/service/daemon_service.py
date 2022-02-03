import util
from model.daemon import PrivyDaemon
import subprocess
import logging

from model.user import PrivyUser

image_name = "godraadam/privyd:alpha"
default_port = 6131

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def start_daemon(daemon: PrivyDaemon, user: PrivyUser):
    logger.info(f"Starting daemon {daemon.name} for user {user.username}")

    # get an available port for the daemon
    port = util.get_available_port()
    
    logger.info(f"Selected port {port}")
    # TODO: move seed derivation to separate function
    if daemon.type == "origin" or daemon.type == "remote":
        # derive seed
        seed = util.derive_seed(user.username, user.password)

        # try creating container
        status = subprocess.run(
            f"docker container create -p {port}:{default_port} --name {daemon.name} -e SEED={seed} -e NODE_TYPE={daemon.type} -e REPO={daemon.repo} {image_name}",
            shell=True,
            capture_output=True,
        )

        # check response
        response = status.stderr.decode("utf-8")
        if response.find(f'"/{daemon.name}" is already in use') >= 0:
            logger.info("Container already exists!")
        elif len(response) > 0:
            # some other error
            logger.error(response)
            return

        # start container (regardless whether creation errored out or not)
        logger.info("Starting container...")
        subprocess.Popen(f"docker start {daemon.name}", shell=True, stdout=subprocess.DEVNULL)
    elif daemon.type == "proxy":

        status = subprocess.run(
            f"docker run -p {port}:{default_port} -- name {daemon.name} -e NODE_TYPE={daemon.type} -e REPO={daemon.repo} -e PUBKEY={daemon.pubkey} {image_name}",
            shell=True,
            capture_output=True,
        )
        # check response
        response = status.stderr.decode("utf-8")
        if response.find(f'"/{daemon.name}" is already in use') >= 0:
            logger.info("Container already exists!")
        elif len(response) > 0:
            # some other error
            logger.error(response)
            return

        # start container (regardless whether creation errored out or not)
        logger.info("Starting container...")
        subprocess.Popen(f"docker start {daemon.name}", shell=True, stdout=subprocess.DEVNULL)
    else:
        logger.error("Unrecognized daemon type")


def start_daemons_for_user(user: PrivyUser):
    logger.info(f"Starting daemons for {user.username}")
    for daemon in user.daemons:
        start_daemon(daemon, user)
        
def remove_daemons_for_user(user: PrivyUser):
    logger.info(f"Removing daemons for {user.username}")
    for daemon in user.daemons:
        subprocess.Popen(f"docker container rm -f {daemon.name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
