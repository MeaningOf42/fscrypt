from . import crypto_utils
from typing import Callable
import os
from pathlib import Path


def map_file(
    oldPath: str | Path, newPath: str | Path, function: Callable[[str], str]
) -> None:
    # Read the old file
    with open(oldPath, "r") as oldFile:
        oldFileText: str = oldFile.read()

    # encrypt the message
    encryptedText = function(oldFileText)

    # save encrypted message to new file
    with open(newPath, "w") as newFile:
        newFile.write(encryptedText)


def map_dir(
    inputDirectory: str | Path,
    outputDirectory: str | Path,
    function: Callable[[str], str],
):
    # Runs checks sanity checks on inputs
    if not os.path.exists(inputDirectory):
        raise RuntimeError(
            f"Given input directory: {inputDirectory} does not seem to exist"
        )
    if os.path.isfile(inputDirectory):
        raise RuntimeError(
            f"Given input directory: {inputDirectory} is a file not a directory"
        )
    if os.path.isfile(outputDirectory):
        raise RuntimeError(
            f"Given output directory: {outputDirectory} is a file not a directory"
        )

    # check if output directory already exists, if it does, delete it. Then create
    # a new and clean output directory
    if os.path.isdir(outputDirectory):
        os.rmdir(outputDirectory)
    os.makedirs(outputDirectory)

    # get all files in the directory, and map them
    files = os.listdir(inputDirectory)
    for file in files:
        if os.path.isdir(os.path.join(inputDirectory, file)):
            map_dir(
                os.path.join(inputDirectory, file),
                os.path.join(outputDirectory, file),
                function,
            )
        else:
            map_file(
                os.path.join(inputDirectory, file),
                os.path.join(outputDirectory, file),
                function,
            )


def strip_commenting(commented_line: str) -> str:
    return commented_line


def encrypt_file_text_from_last_line(input_text: str) -> str:
    """split text into first and last lines and use last line to encrypt others"""
    lines: list[str] = input_text.split("\n")
    body: str = "\n".join(lines[:-1])
    password: str = strip_commenting(lines[-1])
    outputText: str = crypto_utils.encryptStringFromPassword(body, password)
    return outputText


def encryptor_from_password(password: str) -> Callable[[str], str]:
    def encrypt_with_curried_password(plaintext: str) -> str:
        return crypto_utils.encryptStringFromPassword(plaintext, password)

    return encrypt_with_curried_password


def encrypt_file_from_last_line(inputFile: str | Path, outputFile: str | Path) -> None:
    map_file(inputFile, outputFile, encrypt_file_text_from_last_line)


def encrypt_file_from_password(
    inputFile: str | Path, outputFile: str | Path, password: str
) -> None:
    map_file(inputFile, outputFile, encryptor_from_password(password))


def encrypt_files_in_dir_from_last_lines(
    inputDirectory: str | Path, outputDirectory: str | Path
) -> None:
    map_dir(inputDirectory, outputDirectory, encrypt_file_text_from_last_line)


def encrypt_files_in_dir_from_password(
    inputDirectory: str | Path, outputDirectory: str | Path, password: str
) -> None:
    map_dir(inputDirectory, outputDirectory, encryptor_from_password(password))
