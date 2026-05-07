"""
Cryptography utility used to generate
"""

import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode as b64e
from base64 import urlsafe_b64decode as b64d


KEY_DERIVE_ITERATIONS = 480_000


def b64encodeString(toEncode: bytes) -> str:
    return b64e(toEncode).decode("utf-8")


def b64decodeString(toDecode: str) -> bytes:
    if isinstance(toDecode, str):
        raise TypeError("b64decodeString takes a string as input")
    return b64d(bytes(toDecode, "utf-8"))


SALT_BYTES_LEN = 16
SALT_STR_LEN = len(b64encodeString(os.urandom(SALT_BYTES_LEN)))


def genKeyFromPasswordAndSalt(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KEY_DERIVE_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def encryptStringFromPassword(stringToEncrypt: str, password: str) -> str:
    salt: bytes = os.urandom(SALT_BYTES_LEN)
    saltString = b64encodeString(salt)
    key: bytes = genKeyFromPasswordAndSalt(password, salt)
    bytesToEncrypt: bytes = stringToEncrypt.encode("utf-8")
    encryptedMessageString: str = b64encodeString(
        Fernet(b64e(key)).encrypt(bytesToEncrypt)
    )
    return saltString + encryptedMessageString


def decryptStringFromPassword(encryptedString: str, password: str) -> str:
    encryptedMessage: bytes = b64decodeString(encryptedString[SALT_STR_LEN:])
    salt: bytes = b64decodeString(encryptedString[:SALT_STR_LEN])
    key: bytes = genKeyFromPasswordAndSalt(password, salt)

    return Fernet(b64e(key)).decrypt(encryptedMessage).decode("utf-8")
