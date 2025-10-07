"""Automation sessions for the KI-Dev-Tycoon UI project."""

from __future__ import annotations

import nox

SRC_PATHS = ["src", "tests"]

nox.options.sessions = ["lint", "typecheck", "tests", "build"]
nox.options.reuse_existing_virtualenvs = True


def _poetry_install(session: nox.Session) -> None:
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
    """Run mypy with strict settings."""

    _poetry_install(session)
    session.run("poetry", "run", "mypy", "src", external=True)


@nox.session
def tests(session: nox.Session) -> None:
    """Execute the pytest suite."""

    _poetry_install(session)
    session.run("poetry", "run", "pytest", "-q", external=True)


@nox.session
def build(session: nox.Session) -> None:
    """Create a PyInstaller build as smoke test."""

    _poetry_install(session)
    session.run("poetry", "run", "pip", "install", "pyinstaller>=6.0,<7", external=True)
    dist_dir = "dist/nox"
    work_dir = "build/nox"
    session.run(
        "poetry",
        "run",
        "python",
        "tools/build_app.py",
        "--mode",
        "onedir",
        "--dist",
        dist_dir,
        "--work",
        work_dir,
        "--spec",
        work_dir,
        external=True,
    )
    session.run(
        "poetry",
        "run",
        "python",
        "-c",
        "from pathlib import Path; target = Path('dist') / 'nox' / 'ki-dev-tycoon';"
        "assert target.exists() and target.is_dir()",
        external=True,
    )
