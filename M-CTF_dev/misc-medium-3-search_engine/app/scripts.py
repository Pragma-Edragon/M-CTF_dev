def get_hex(number: int):
    return "0x{0:04x}".format(number)


def random_hex(number: str):
    return "0x{0:06x}".format(ord(number))