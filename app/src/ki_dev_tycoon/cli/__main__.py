"""Command line entrypoint for packaging."""

from __future__ import annotations

from .ui_commands import app


def main() -> None:
    """Execute the Typer application."""

    app()


if __name__ == "__main__":  # pragma: no cover - exercised in packaging builds
    main()
