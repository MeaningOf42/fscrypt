from pathlib import Path
from typing import Annotated, Callable

import typer

from . import crypto_utils
from . import file_tools

app = typer.Typer(help="Encrypt and decrypt text files.")


@app.command()
def encrypt_file(
    input_file: Annotated[Path, typer.Argument(help="plaintext input file")],
    output_file: Annotated[Path, typer.Argument(help="plaintext input file")],
    password: Annotated[
        str | None,
        typer.Option(
            "--password",
            "-p",
            help="Password to use. If ommited the last line of the file is used",
        ),
    ] = None,
) -> None:
    """
    Encrypt one file with last line.

    If --password is omitted, the final line of the input file is used as the password.
    """

    # Create a encryption function that either uses the last line of text, or password if password is given
    encryption_function: Callable[[str], str]
    if password is None:
        encryption_function = file_tools.encrypt_file_text_from_last_line
    else:
        given_password: str = password

        def encryption_function(plaintext: str) -> str:
            return crypto_utils.encryptStringFromPassword(plaintext, given_password)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    file_tools.map_file(input_file, output_file, encryption_function)

    password_explaination: str = "the last line in in the file"
    if password is not None:
        password_explaination = password

    typer.echo(
        f"Encrypted {input_file} -> {output_file} using {password_explaination} as the password"
    )


@app.command()
def encrypt_dir(
    input_directory: Annotated[
        Path,
        typer.Argument(
            help="dir full of plaintext input files with the password to each as the last line of text"
        ),
    ],
    output_directory: Annotated[
        Path,
        typer.Argument(help="output directory where encrypted files will be placed"),
    ],
) -> None:
    "Recreate structure of input directory in output director, but every file is encrypted" " with the last line of text used as a password."
    file_tools.map_dir(
        input_directory, output_directory, file_tools.encrypt_file_text_from_last_line
    )
