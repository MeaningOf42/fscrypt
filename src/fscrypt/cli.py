from pathlib import Path
from typing import Annotated

import typer

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
    # Creates the parent directory of the output file
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # If there is a password create a encrypted file using it, if not encrypt using the last line of the file
    if password is None:
        file_tools.encrypt_file_from_last_line(input_file, output_file)
    else:
        given_password: str = password
        file_tools.encrypt_file_from_password(input_file, output_file, given_password)

    # Prints out a message saying what file was encrypted and using what password:
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
    password: Annotated[
        str | None,
        typer.Option(
            "--password",
            "-p",
            help="Password to use. If ommited the last line of each file is used",
        ),
    ] = None,
) -> None:
    "Recreate structure of input directory in output director, but every file is encrypted with the last line of text used as a password."
    if password is None:
        file_tools.encrypt_files_in_dir_from_last_lines(
            input_directory, output_directory
        )
    else:
        file_tools.encrypt_files_in_dir_from_password(
            input_directory, output_directory, password
        )
