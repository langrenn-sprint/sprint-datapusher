"""Module for cli application monitoring directory and send json to webserver."""
import logging
import os
import time
from typing import Any

import click
from dotenv import load_dotenv
import pandas as pd
import requests
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from . import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
load_dotenv()
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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
    # Check if webserver is alive:
    if _webserver_allive(url):
        click.echo(f"\nWorking directory {os.getcwd()}")
        click.echo(f"Watching directory {os.path.join(os.getcwd(), directory)}")
        click.echo(f"Sending data to webserver at {url}")
    else:
        exit(2)

    monitor = FileSystemMonitor(directory=directory, url=url)
    monitor.start(loop_action=lambda: time.sleep(1))

    click.echo("Bye!\n")


def _webserver_allive(url: str) -> bool:
    try:
        _url = f"{url}/ping"
        logging.debug(f"Trying to ping webserver at {url}")
        response = requests.get(_url)
        if response.status_code == 200:
            logging.info(f"Connected to {url}")
            return True
        else:
            logging.error(
                f"Webserver respondend with not ok status_code: {response.status_code}"
            )
    except Exception:
        logging.error("Webserver not available. Exiting....")
    return False


class FileSystemMonitor:
    """Monitor directory and send content of files as json to webserver URL."""

    def __init__(self, url: str, directory: Any) -> None:
        """Initalize the monitor."""
        self.url = url
        self.path = directory
        self.handler = EventHandler(url)

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

    def __init__(self, url: str) -> None:
        """Initalize the monitor."""
        super(EventHandler, self).__init__()
        self.url = url

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

        if not event.is_directory:
            _convert_and_push_data(self.url, event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        super(EventHandler, self).on_modified(event)

        if not event.is_directory:
            _convert_and_push_data(self.url, event.src_path)


def _convert_and_push_data(url: str, src_path: Any) -> None:
    # read the csv into a dataframe:

    url = f"{url}/klasser"
    body = _convert_csv_to_json(src_path)
    headers = {"content-type": "application/json; charset=utf-8"}
    logging.debug(f"sending body {body}")
    try:
        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 201:
            logging.debug(f"Converted and pushed {src_path} -> {response.status_code}")
        else:
            logging.error(f"got status {response.status_code}")
    except Exception as e:
        logging.error(f"got exceptions {e}")


def _convert_csv_to_json(src_path: str) -> str:
    # TODO this code must be adapted to different types of files
    df = pd.read_csv(src_path, sep=";", encoding="utf-8")
    # filter out irrelevant data:
    df = df.iloc[1:]  # drops the first row
    df.dropna(subset=["Klasse"], inplace=True)  # drops all rows with no value in Klasse
    df.dropna(how="all", axis="columns", inplace=True)  # drops columns with no values
    df.reset_index(drop=True, inplace=True)  # resets index
    # set the url for this object
    # --- END TODO ---

    # convert dataframe to json
    logging.debug(f"df before converting to json {df}")
    return df.to_json(orient="records", force_ascii=True)
