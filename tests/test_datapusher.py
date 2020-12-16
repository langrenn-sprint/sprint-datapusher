"""Unit test cases for the generateSpecification module."""
import os

from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture

from sprint_datapusher.datapusher import cli, FileSystemMonitor


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def fake_loop_action() -> None:
    """Fake loop action."""
    raise KeyboardInterrupt


def test_FileSystemMonitor_with_url_arguments_succeds(runner: CliRunner) -> None:
    """Should return exit_code 0."""
    url = "http://example.com"
    monitor = FileSystemMonitor(url, os.getcwd())
    monitor.start(loop_action=fake_loop_action)

    pass


def test_cli_with_url_arguments_and_directory_succeds(runner: CliRunner) -> None:
    """Should return exit_code 0."""
    directory = "tests/files"
    url = "http://example.com"

    monitor = FileSystemMonitor(url, directory)
    monitor.start(loop_action=fake_loop_action)

    pass


# --- Bad cases ---
def test_cli_no_arguments_fails(runner: CliRunner) -> None:
    """Should return exit_code 2."""
    runner = CliRunner()

    result = runner.invoke(cli)
    assert "Error: Missing argument 'URL'" in result.output
    assert result.exit_code == 2


def test_cli_option_directory_does_not_exist(
    mocker: MockFixture, runner: CliRunner
) -> None:
    """Should return exit_code 0."""
    runner = CliRunner()

    result = runner.invoke(cli, ["-d does_not_exist"])
    assert "does not exist" in result.output
    assert result.exit_code == 2
