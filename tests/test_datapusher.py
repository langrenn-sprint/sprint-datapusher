"""Unit test cases for the generateSpecification module."""
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture
from sprint_datapusher.datapusher import main


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_no_arguments_succeeds(runner: CliRunner) -> None:
    """Should return exit_code 2."""
    runner = CliRunner()

    result = runner.invoke(main)
    assert result.output == ""
    assert result.exit_code == 0


def test_main_option_folder_does_not_exist(
    mocker: MockFixture, runner: CliRunner
) -> None:
    """Should return exit_code 0."""
    runner = CliRunner()

    result = runner.invoke(main, ["-d folder"])
    assert "does not exist" in result.output
    assert result.exit_code == 2
