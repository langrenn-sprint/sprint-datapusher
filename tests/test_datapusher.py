"""Unit test cases for the generateSpecification module."""
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture

from sprint_datapusher.datapusher import main


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_with_url_arguments_succeds(runner: CliRunner) -> None:
    """Should return exit_code 0."""
    runner = CliRunner()

    result = runner.invoke(main, ["http://example.com"])
    assert "Watching directory ./" in result.output
    assert "Sending data to webserver at http://example.com" in result.output
    assert result.exit_code == 0


def test_main_no_arguments_fails(runner: CliRunner) -> None:
    """Should return exit_code 2."""
    runner = CliRunner()

    result = runner.invoke(main)
    assert "Error: Missing argument 'URL'" in result.output
    assert result.exit_code == 2


def test_main_option_directory_does_not_exist(
    mocker: MockFixture, runner: CliRunner
) -> None:
    """Should return exit_code 0."""
    runner = CliRunner()

    result = runner.invoke(main, ["-d does_not_exist"])
    assert "does not exist" in result.output
    assert result.exit_code == 2
