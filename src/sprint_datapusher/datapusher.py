"""Module for cli application monitoring directory and send json to webserver."""
import logging
import os
import time
from typing import Any

import click
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

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
def cli(url: str, directory: Any) -> None:
    """CLI for monitoring directory and send content of files as json to webserver URL.

    URL is the url to a webserver exposing an endpoint accepting your json.

    To stop the datapusher, press Control-C.
    \f
    Args:
        url: the URL to a webserver exposing an endpoint accepting your json.
        directory: relative path to the directory to watch
    """  # noqa: D301
    click.echo(f"\nWorking directory {os.getcwd()}")
    click.echo(f"Watching directory {os.path.join(os.getcwd(), directory)}")
    click.echo(f"Sending data to webserver at {url}")

    monitor = FileSystemMonitor(directory=directory, url=url)
    monitor.start(loop_action=lambda: time.sleep(1))


class FileSystemMonitor:
    """Monitor directory and send content of files as json to webserver URL."""

    def __init__(self, url: str, directory: Any) -> None:
        """Initalize the monitor."""
        self.url = url
        self.path = directory
        self.handler = EventHandler()

    def start(self, loop_action: Any) -> None:
        """Start the monitor."""
        observer = Observer()
        observer.schedule(self.handler, self.path, recursive=True)
        observer.start()
        try:
            while True:
                loop_action()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class EventHandler(FileSystemEventHandler):
    """Custom eventhandler class."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    def on_any_event(self, event: FileSystemEvent) -> None:
        """Handle any events primarily for logging."""
        super(EventHandler, self).on_any_event(event)

        what = "directory" if event.is_directory else "file"
        logging.info(
            f"{event.event_type} {what}: {event.src_path}",
        )

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        super(EventHandler, self).on_created(event)

        what = "directory" if event.is_directory else "file"
        logging.info(
            f"{event.event_type} {what}: {event.src_path}",
        )
