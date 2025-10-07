"""PyInstaller build orchestration for the KI Dev Tycoon UI."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Iterable, Sequence

try:
    from PyInstaller.__main__ import run as pyinstaller_run
except ImportError as exc:  # pragma: no cover - handled in CLI entrypoint
    pyinstaller_run = None


REPO_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = REPO_ROOT / "app"
SRC_ROOT = APP_ROOT / "src"
DEFAULT_ENTRY = SRC_ROOT / "ki_dev_tycoon" / "cli" / "__main__.py"
ASSET_ROOT = REPO_ROOT / "assets"


def _resolve_version(explicit: str | None) -> str:
    if explicit:
        return explicit
    try:
        from ki_dev_tycoon import __version__
    except Exception:  # pragma: no cover - editable installs during CI
        return "0.0.0"
    return __version__


def _collect_add_data(asset_paths: Iterable[Path]) -> list[str]:
    bundles: list[str] = []
    for path in asset_paths:
        if not path.exists():
            continue
        destination = path.name
        bundles.append(f"{path}{os.pathsep}{destination}")
    return bundles


def _write_version_metadata(target: Path, version: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"{version}\n", encoding="utf-8")


def _copy_support_files(dist_dir: Path, mode: str) -> None:
    licence_src = REPO_ROOT / "LICENSE"
    if licence_src.exists():
        shutil.copy2(licence_src, dist_dir / "LICENSE")
    readme_src = APP_ROOT / "README.md"
    if readme_src.exists():
        shutil.copy2(readme_src, dist_dir / "README.md")
    if ASSET_ROOT.exists() and mode == "onedir":
        target_assets = dist_dir / "assets"
        if target_assets.exists():
            shutil.rmtree(target_assets)
        shutil.copytree(ASSET_ROOT, target_assets)


def build_application(
    *,
    mode: str,
    dist_dir: Path,
    work_dir: Path,
    spec_dir: Path,
    icon: Path | None,
    version: str,
    name: str,
    entry: Path,
    assets: Sequence[Path],
    clean: bool,
    dry_run: bool,
) -> Path:

    dist_dir = dist_dir.expanduser().resolve()
    work_dir = work_dir.expanduser().resolve()
    spec_dir = spec_dir.expanduser().resolve()
    entry = entry.expanduser().resolve()

    if not entry.exists():
        msg = f"Entry script {entry} does not exist"
        raise FileNotFoundError(msg)

    command: list[str] = [
        f"--distpath={dist_dir}",
        f"--workpath={work_dir}",
        f"--specpath={spec_dir}",
        f"--name={name}",
    ]
    if clean:
        command.append("--clean")
    if mode == "onefile":
        command.append("--onefile")
    elif mode != "onedir":
        msg = f"Unsupported build mode: {mode}"
        raise ValueError(msg)
    if icon is not None:
        icon_path = icon.expanduser().resolve()
        if not icon_path.exists():
            msg = f"Icon file {icon_path} not found"
            raise FileNotFoundError(msg)
        command.append(f"--icon={icon_path}")

    for data in _collect_add_data(assets):
        command.append(f"--add-data={data}")

    command.append(str(entry))

    if dry_run:
        print("PyInstaller command:", "pyinstaller", *command)
        return dist_dir / name

    if pyinstaller_run is None:
        msg = "PyInstaller is not available. Install it or pass --dry-run."
        raise RuntimeError(msg)

    pyinstaller_run(command)

    target = dist_dir / name
    if mode == "onefile" and target.is_file():
        version_file = target.with_name(f"{target.stem}_VERSION.txt")
    else:
        target.mkdir(exist_ok=True)
        version_file = target / "VERSION.txt"
    _write_version_metadata(version_file, version)
    _copy_support_files(target if target.is_dir() else target.parent, mode)
    return target


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build PyInstaller artefacts for the UI")
    parser.add_argument("--mode", choices=["onefile", "onedir"], default="onedir")
    parser.add_argument("--dist", type=Path, default=APP_ROOT / "dist")
    parser.add_argument("--work", dest="work", type=Path, default=APP_ROOT / "build")
    parser.add_argument("--spec", dest="spec", type=Path, default=APP_ROOT / "build")
    parser.add_argument("--icon", type=Path, default=None)
    parser.add_argument("--version", type=str, default=None)
    parser.add_argument("--name", type=str, default="ki-dev-tycoon")
    parser.add_argument("--entry", type=Path, default=DEFAULT_ENTRY)
    parser.add_argument(
        "--assets",
        type=Path,
        nargs="*",
        default=[ASSET_ROOT],
        help="Additional asset directories to bundle.",
    )
    parser.add_argument("--no-clean", action="store_false", dest="clean")
    parser.add_argument("--dry-run", action="store_true")
    parser.set_defaults(clean=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    version = _resolve_version(args.version)
    assets = list(args.assets)
    try:
        build_application(
            mode=args.mode,
            dist_dir=args.dist,
            work_dir=args.work,
            spec_dir=args.spec,
            icon=args.icon,
            version=version,
            name=args.name,
            entry=args.entry,
            assets=assets,
            clean=args.clean,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # pragma: no cover - exercised via CLI
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover - manual execution
    raise SystemExit(main())
