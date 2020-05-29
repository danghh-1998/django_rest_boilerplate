import binascii
import os


def generate_token(length):
    return binascii.hexlify(os.urandom(length)).decode()
