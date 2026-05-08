import random
import string

PLAINTEXT_TEST_FILES: list[tuple[str, str, str]] = [
    ("message1.txt", "Love letter from Bob to Alice, very secure!", "pass1"),
    ("message2.txt", "Dear Bob, I am glad to hear you feel the same way", "pass2"),
    ("message3.txt", "Let's go watch a movie together on friday?\npass3", "pass3"),
    ("diary/entry1.txt", "I have such a crush on bob", "AKfmcIodlp98720"),
    (
        "diary/entry2.txt",
        "I hope he feels the same way about me\npass3",
        "Very Long Password!!!udksPOldSuper3Secure",
    ),
    (
        "diary/super_secret/self_only.txt",
        "my RSA primes are 67 and 722896686382073903939970876463",
        "67722896686382073903939970876463",
    ),
]


def create_random_string(
    length: int, alphabet=string.ascii_letters + string.digits
) -> str:
    return "".join([random.choice(alphabet) for _ in range(length)])


def fake_encryption(plaintext: str) -> str:
    return f"ENCRYPTED({plaintext})"
