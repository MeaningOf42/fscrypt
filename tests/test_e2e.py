from pathlib import Path
import subprocess
from testing_utils import PLAINTEXT_TEST_FILES
from fscrypt.crypto_utils import decryptStringFromPassword


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["fscrypt", *args], text=True, capture_output=True, check=False
    )


def test_encrypt_file_with_pass_e2e(tmp_path: Path):
    password: str = "S3cur3P4ss123!"
    plaintext: str = "secrete message from alice to bob"
    input_file = tmp_path / "plain_text.txt"
    input_file.write_text(plaintext)
    output_file = tmp_path / "output_file.txt"

    result = run_cli("encrypt-file", str(input_file), str(output_file), "-p", password)

    assert result.returncode == 0
    assert output_file.exists()
    assert decryptStringFromPassword(output_file.read_text(), password) == plaintext
    assert "Encrypted" in result.stdout


def test_encrypt_file_with_no_pass_e2e(tmp_path: Path):
    password: str = "S3cur3P4ss123!"
    plaintext: str = "secrete message from alice to bob"
    body: str = plaintext + "\n" + password
    input_file = tmp_path / "plain_text.txt"
    input_file.write_text(body)
    output_file = tmp_path / "output_file.txt"

    result = run_cli("encrypt-file", str(input_file), str(output_file))

    assert result.returncode == 0
    assert output_file.exists()
    assert decryptStringFromPassword(output_file.read_text(), password) == plaintext
    assert "Encrypted" in result.stdout


def test_encrypt_dir_recursive_e2e(tmp_path: Path):
    for filepath, plaintext, password in PLAINTEXT_TEST_FILES:
        filebody: str = plaintext + "\n" + password
        full_filepath: Path = tmp_path / "plain_dir" / filepath
        full_filepath.parent.mkdir(parents=True, exist_ok=True)
        full_filepath.write_text(filebody)

    run_cli("encrypt-dir", str(tmp_path / "plain_dir"), str(tmp_path / "crypt_dir"))

    for path, contents, password in PLAINTEXT_TEST_FILES:
        full_filepath = tmp_path / "crypt_dir" / path
        assert full_filepath.exists()
        encrypted: str = full_filepath.read_text()
        decrypted: str = decryptStringFromPassword(encrypted, password)
        assert decrypted == contents
