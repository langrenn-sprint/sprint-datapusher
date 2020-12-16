"""Module for generate openAPI specifications."""
import os
from typing import Any

import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
@click.option(
    "-d",
    "--directory",
    default=".",
    help="The directory to watch",
    show_default=True,
    type=click.Path(
        exists=True,
        file_okay=False,
        writable=True,
    ),
)
def main(directory: Any) -> None:
    """Write specification and catalog file based on template for bank."""
    # Add a trailing slash to directory if not there:
    directory = os.path.join(directory, "")
