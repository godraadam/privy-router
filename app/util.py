import base64
from hashlib import scrypt
import socket


def derive_seed(username: str, password: str) -> str:
    return base64.b64encode(
        scrypt(
            password=password.encode("utf-8"),
            salt=username.encode("utf-8"),
            dklen=64,
            n=8,
            r=8,
            p=1,
        )
    ).decode("utf-8")


def get_available_port(start: int = 6131) -> int:
    port = start
    while True:
        try:
            s = socket.socket()  # create a socket object
            s.bind(("127.0.0.1", port))  # test the port
            s.close()
            break
        except Exception:
            port += 1
    return port
