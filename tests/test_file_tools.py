from pathlib import Path
from pyfakefs.fake_filesystem import FakeFilesystem
from testing_utils import fake_encryption, PLAINTEXT_TEST_FILES

import fscrypt.file_tools as file_tools
import fscrypt.crypto_utils as crypto_utils


def test_map_file_transforms_file(fs: FakeFilesystem) -> None:
    plaintext_test_message: str = (
        "Love letter from Bob to Alice, Very important to be kept Secure!"
    )

    fs.create_file("plaintext.txt", contents=plaintext_test_message)

    file_tools.map_file("plaintext.txt", "encrypted.txt", fake_encryption)

    assert Path("/plaintext.txt").read_text() == plaintext_test_message
    assert Path("/encrypted.txt").read_text() == fake_encryption(plaintext_test_message)


def test_map_dir_transforms_nested_dir(fs: FakeFilesystem) -> None:
    for path, contents, _ in PLAINTEXT_TEST_FILES:
        fs.create_file(Path("/plaintext_dir") / path, contents=contents)

    file_tools.map_dir("/plaintext_dir", "/encrypted_dir", fake_encryption)

    for path, contents, _ in PLAINTEXT_TEST_FILES:
        assert (Path("/encrypted_dir") / path).read_text() == fake_encryption(contents)


def test_encrypt_all_files_in_dir_with_fake_dir(fs: FakeFilesystem) -> None:
    for path, contents, password in PLAINTEXT_TEST_FILES:
        fs.create_file(
            Path("/plaintext_dir") / path, contents=contents + "\n" + password
        )

    file_tools.encrypt_all_files_in_dir("/plaintext_dir", "/encrypted_dir")

    for path, contents, password in PLAINTEXT_TEST_FILES:
        encrypted: str = (Path("/encrypted_dir") / path).read_text()
        decrypted: str = crypto_utils.decryptStringFromPassword(encrypted, password)
        assert decrypted == contents
