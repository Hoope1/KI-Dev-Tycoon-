"""Automation sessions for the KI-Dev-Tycoon simulation package."""

from __future__ import annotations

import nox

SRC_PATHS = ["src", "tests"]

nox.options.sessions = ["lint", "typecheck", "tests"]
nox.options.reuse_existing_virtualenvs = True


def _poetry_install(session: nox.Session) -> None:
    """Install project dependencies via Poetry inside the session."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "dev", external=True)


@nox.session
def lint(session: nox.Session) -> None:
    """Run Ruff, Black and isort in check mode."""
    _poetry_install(session)
    session.run("poetry", "run", "ruff", "check", *SRC_PATHS, external=True)
    session.run("poetry", "run", "black", "--check", *SRC_PATHS, external=True)
    session.run("poetry", "run", "isort", "--check-only", *SRC_PATHS, external=True)


@nox.session
def typecheck(session: nox.Session) -> None:
    """Run mypy with the strict configuration."""
    _poetry_install(session)
    session.run("poetry", "run", "mypy", "src", external=True)


@nox.session
def tests(session: nox.Session) -> None:
    """Execute the pytest suite."""
    _poetry_install(session)
    session.run("poetry", "run", "pytest", "-q", external=True)
