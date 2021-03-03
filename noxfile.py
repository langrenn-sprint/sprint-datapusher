"""Nox sessions."""
import tempfile

import nox
from nox.sessions import Session
import nox_poetry  # noqa: F401

package = "sprint_datapusher"
locations = "src", "tests", "noxfile.py"
nox.options.stop_on_first_error = True
nox.options.sessions = ("black", "lint")


@nox.session(python=["3.7", "3.9"])
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python=["3.7", "3.9"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
        "flake8-assertive",
        "pep8-naming",
    )
    session.run("flake8", *args)
