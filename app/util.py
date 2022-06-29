from base64 import b64encode
from hashlib import sha256
import socket
from mnemonic import Mnemonic

mnemo = Mnemonic("english")

def hash(key: str) -> str:
    m = sha256()
    m.update(key)
    return b64encode(m.digest()).decode('utf-8')

def derive_seed(mnemonic: str) -> str:
    return b64encode(mnemo.to_seed(mnemonic, "")).decode('utf-8')


def get_mnemonic():
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=128)
    return words

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
