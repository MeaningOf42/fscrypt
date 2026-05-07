from crypto_utils import (
    decryptStringFromPassword,
    encryptStringFromPassword,
    b64decodeString,
    b64encodeString,
)
import unittest
import os
import random
import string


b64Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"


def create_random_string(
    length: int, alphabet=string.ascii_letters + string.digits
) -> str:
    return "".join([random.choice(alphabet) for _ in range(length)])


class TestB64StringUtils(unittest.TestCase):
    def test_encode_decode(self) -> None:
        """Checks that you can encode then decode bytes and end up with the same bytes"""
        testBytes: bytes = os.urandom(16)
        encodeDecode: bytes = b64decodeString(b64encodeString(testBytes))
        self.assertEqual(testBytes, encodeDecode)

    def test_decode_encode(self) -> None:
        """Checks that you can decode then encode a string and end up with the same string"""
        for i in range(100):
            testString: str = "".join([random.choice(b64Chars) for i in range(16)])
            decodeEncode: str = b64encodeString(b64decodeString(testString))
            self.assertEqual(testString, decodeEncode)


class TestPasswordEncryptionDecryption(unittest.TestCase):
    def testEncryptDecript(self):
        password: str = create_random_string(10)
        secretMessage: str = f"""

Dear bob,

this is my secret message to confess my love to you! also here is a random string {create_random_string(10)}.

Yours faithfully,

Alice

"""
        encryptedMessage: str = encryptStringFromPassword(secretMessage, password)
        decryptedMessage: str = decryptStringFromPassword(encryptedMessage, password)
        self.assertEqual(secretMessage, decryptedMessage)


class TestExceptions(unittest.TestCase):
    def testB64DecodeStringThrowsTypeError(self):
        """Checks that b64decode string throws error as Runtime Error"""
        with self.assertRaises(TypeError):
            b64decodeString(os.urandom(16))


if __name__ == "__main__":
    unittest.main()
