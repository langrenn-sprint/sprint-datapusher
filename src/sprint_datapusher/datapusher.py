"""Module for cli application monitoring directory and send json to webserver."""
import os
from typing import Any

import click

from . import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.argument("url", type=click.STRING)
@click.option(
    "-d",
    "--directory",
    default=os.getcwd(),
    help="Relative path to the directory to watch",
    show_default=True,
    type=click.Path(
        exists=True,
        file_okay=False,
    ),
)
def main(url: str, directory: Any) -> None:
    """Monitor directory and send content of files as json to webserver URL.

    URL is the url to a webserver exposing an endpoint accepting your json.
    \f
    Args:
        url: the URL to a webserver exposing an endpoint accepting your json.
        directory: relative path to the directory to watch
    """  # noqa: D301
    click.echo(f"\nWorking directory {os.getcwd()}")
    click.echo(f"Watching directory {os.path.join(os.getcwd(), directory)}")
    click.echo(f"Sending data to webserver at {url}")
