from pathlib import Path
from pyfakefs.fake_filesystem import FakeFilesystem

import fsencrypt.file_tools as file_tools
import fsencrypt.crypto_utils as crypto_utils


def fake_encryption(plaintext: str) -> str:
    return f"ENCRYPTED({plaintext})"


plaintext_test_files: list[tuple[str, str, str]] = [
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


def test_map_file_transforms_file(fs: FakeFilesystem) -> None:
    plaintext_test_message: str = (
        "Love letter from Bob to Alice, Very important to be kept Secure!"
    )

    fs.create_file("plaintext.txt", contents=plaintext_test_message)

    file_tools.map_file("plaintext.txt", "encrypted.txt", fake_encryption)

    assert Path("/plaintext.txt").read_text() == plaintext_test_message
    assert Path("/encrypted.txt").read_text() == fake_encryption(plaintext_test_message)


def test_map_dir_transforms_nested_dir(fs: FakeFilesystem) -> None:
    for path, contents, _ in plaintext_test_files:
        fs.create_file(Path("/plaintext_dir") / path, contents=contents)

    file_tools.map_dir("/plaintext_dir", "/encrypted_dir", fake_encryption)

    for path, contents, _ in plaintext_test_files:
        assert (Path("/encrypted_dir") / path).read_text() == fake_encryption(contents)


def test_encrypt_all_files_in_dir_with_fake_dir(fs: FakeFilesystem) -> None:
    for path, contents, password in plaintext_test_files:
        fs.create_file(
            Path("/plaintext_dir") / path, contents=contents + "\n" + password
        )

    file_tools.encrypt_all_files_in_dir("/plaintext_dir", "/encrypted_dir")

    for path, contents, password in plaintext_test_files:
        encrypted: str = (Path("/encrypted_dir") / path).read_text()
        decrypted: str = crypto_utils.decryptStringFromPassword(encrypted, password)
        assert decrypted == contents
