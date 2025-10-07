"""SteamCMD automation helpers for distributing the UI builds."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Sequence

DEFAULT_DESCRIPTION = "KI Dev Tycoon nightly build"


def _read_text(path: Path | None) -> str | None:
    """Read optional text file and return stripped contents."""

    if path is None:
        return None
    if not path.exists():
        msg = f"Changelog file {path} not found"
        raise FileNotFoundError(msg)
    return path.read_text(encoding="utf-8").strip()


def _resolve_description(description: str | None, changelog: Path | None) -> str:
    """Derive a release description for the Steam build."""

    if description:
        return description
    changelog_text = _read_text(changelog)
    if changelog_text:
        return changelog_text.splitlines()[0][:120]
    try:
        from ki_dev_tycoon import __version__
    except Exception:  # pragma: no cover - during editable installs
        return DEFAULT_DESCRIPTION
    return f"KI Dev Tycoon {__version__}"


def _build_vdf(
    *,
    app_id: str,
    depot_id: str,
    build_dir: Path,
    output_dir: Path,
    branch: str,
    description: str,
) -> str:
    """Construct the Steam app build configuration."""

    return f"""
"appbuild"
{{
    "appid" "{app_id}"
    "desc" "{description}"
    "buildoutput" "{output_dir.as_posix()}"
    "contentroot" "{build_dir.as_posix()}"
    "setlive" "{branch}"
    "depots"
    {{
        "{depot_id}"
        {{
            "contentroot" "{build_dir.as_posix()}"
            "filemapping"
            {{
                "LocalPath" "*"
                "DepotPath" "."
                "recursive" "1"
            }}
        }}
    }}
}}
""".strip()


def _steam_credentials(username: str | None, password_env: str, guard_env: str) -> tuple[str, str, str | None]:
    """Resolve Steam credentials from CLI arguments and environment variables."""

    resolved_username = username or os.getenv("STEAM_USERNAME")
    if not resolved_username:
        msg = "Steam username not provided"
        raise ValueError(msg)
    password = os.getenv(password_env)
    if not password:
        msg = f"Environment variable {password_env} is required for the password"
        raise ValueError(msg)
    guard = os.getenv(guard_env)
    return resolved_username, password, guard


def _run_steamcmd(
    *,
    steamcmd: Path,
    username: str,
    password: str,
    guard: str | None,
    vdf_path: Path,
    dry_run: bool,
) -> None:
    """Execute SteamCMD with the generated VDF payload."""

    command = [str(steamcmd), "+login", username, password]
    if guard:
        command.append(guard)
    command.extend(["+run_app_build", str(vdf_path), "+quit"])
    if dry_run:
        print("SteamCMD command:", " ".join(command))
        return
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        msg = f"steamcmd failed with exit code {result.returncode}"
        raise RuntimeError(msg)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments for the Steam upload helper."""

    parser = argparse.ArgumentParser(description="Upload PyInstaller builds to Steam")
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--depot-id", required=True)
    parser.add_argument("--branch", default="public")
    parser.add_argument("--steamcmd", type=Path, default=Path("steamcmd"))
    parser.add_argument("--username", type=str, default=None)
    parser.add_argument("--password-env", type=str, default="STEAM_PASSWORD")
    parser.add_argument("--guard-env", type=str, default="STEAM_GUARD")
    parser.add_argument("--description", type=str, default=None)
    parser.add_argument("--changelog", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for invoking SteamCMD uploads."""

    args = parse_args(argv)
    build_dir = args.build_dir.expanduser().resolve()
    if not build_dir.exists():
        print(f"Build directory {build_dir} not found", file=sys.stderr)
        return 1
    description = _resolve_description(args.description, args.changelog)
    try:
        username, password, guard = _steam_credentials(
            args.username, args.password_env, args.guard_env
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        vdf_text = _build_vdf(
            app_id=args.app_id,
            depot_id=args.depot_id,
            build_dir=build_dir,
            output_dir=output_dir,
            branch=args.branch,
            description=description,
        )
        vdf_path = Path(tmpdir) / "app_build.vdf"
        vdf_path.write_text(vdf_text, encoding="utf-8")
        try:
            _run_steamcmd(
                steamcmd=args.steamcmd,
                username=username,
                password=password,
                guard=guard,
                vdf_path=vdf_path,
                dry_run=args.dry_run,
            )
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":  # pragma: no cover - manual execution
    raise SystemExit(main())
