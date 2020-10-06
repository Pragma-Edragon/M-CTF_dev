from cryptography.fernet import Fernet
from base64 import urlsafe_b64decode, urlsafe_b64encode

salt = 'r1v3n-1s-th3-b3st-g1rl-1n-th3-wd'
key = urlsafe_b64encode(bytes(salt, 'utf'))


def encodeData(data: str) -> str:
    # entering string -> returning bytes decoded to string value
    return Fernet(key).encrypt(bytes(data, 'utf')).decode()


def decodeData(data: bytes):
    # entering bytes object -> returning string object
    return Fernet(key).decrypt(data).decode()
