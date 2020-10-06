from app.scripts import random_hex, get_hex
from base64 import encodebytes
from random import randint


def encode_data(data_to_encode: bytes):
    res = ''
    key = randint(1, 3)
    while True:
        if key == 0:
            break
        res += ' '.join(str(''.join(list(map(get_hex, map(ord, str(encodebytes(data_to_encode))))))))
        if key % 2 == 0:
            res += "="
        key -= 1
    return res
