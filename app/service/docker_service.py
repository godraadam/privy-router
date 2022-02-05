import logging
import docker

from model.daemon import PrivyDaemon

logger = logging.getLogger(__name__)

client = docker.from_env()

image_name = "godraadam/privyd:alpha"
default_port = 6131


def create_privyd_container(daemon: PrivyDaemon, seed: str, port:int):

    environments = {
        "origin": {"SEED": seed, "NODE_TYPE": daemon.type, "REPO": daemon.repo},
        "remote": {"SEED": seed, "NODE_TYPE": daemon.type, "REPO": daemon.repo},
        "proxy": {
            "PUBKEY": daemon.proxy_pubkey,
            "NODE_TYPE": daemon.type,
            "REPO": daemon.repo,
        },
    }

    return client.containers.create(
        image_name,
        ports={default_port: f"{port}/tcp"},
        environment=environments[daemon.type],
        name=daemon.name,
    )


def exists_privyd_container(name: str) -> bool:
    try:
        client.containers.get(name)
        return True
    except docker.errors.NotFound:
        return False


def start_privyd_container(name: str):
    try:
        container = client.containers.get(name)
        container.start()
    except docker.errors.NotFound:
        return


def remove_privyd_container(name: str):
    try:
        container = client.containers.get(name)
        container.stop()
        container.remove()
    except docker.errors.NotFound:
        pass
