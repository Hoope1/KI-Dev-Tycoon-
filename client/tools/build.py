#!/usr/bin/env python3
"""Utility to export the Godot client mock for KI-Dev-Tycoon.

The script wraps the Godot CLI to provide a reproducible build pipeline
that can be executed locally or from CI. When the Godot binary is not
available (e.g. on CI smoke runs without the engine), the script falls
back to a mock export that still packages the project assets so that
later steps in the pipeline can operate on deterministic artefacts.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Final

ROOT: Final[Path] = Path(__file__).resolve().parent.parent
PROJECT_DIR: Final[Path] = ROOT / "godot_project"
DEFAULT_BUILD_DIR: Final[Path] = ROOT / "build"
ZIP_NAME_TEMPLATE: Final[str] = "KI-Dev-Tycoon-{export}.zip"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the KI-Dev-Tycoon client mock")
    parser.add_argument(
        "--export",
        choices=("web",),
        default="web",
        help="Name of the export preset to use.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory for the exported artefacts (defaults to build/<export>).",
    )
    parser.add_argument(
        "--godot-bin",
        default=Path(shutil.which("godot4") or "godot4"),
        help="Path to the Godot executable (defaults to `godot4` on PATH).",
    )
    parser.add_argument(
        "--mock-export",
        action="store_true",
        help="Skip the Godot CLI invocation and only create placeholder artefacts.",
    )
    return parser.parse_args()


def ensure_project_exists() -> None:
    if not PROJECT_DIR.exists():
        raise SystemExit(f"Godot project directory not found: {PROJECT_DIR}")


def run_godot_export(godot_bin: str | Path, export_name: str, output_dir: Path) -> bool:
    export_targets = {
        "web": {
            "preset": "Web",
            "filename": "KI-Dev-Tycoon.html",
        }
    }
    target = export_targets[export_name]
    output_file = output_dir / target["filename"]
    cmd = [
        str(godot_bin),
        "--headless",
        "--path",
        str(PROJECT_DIR),
        "--export-release",
        target["preset"],
        str(output_file),
    ]
    try:
        subprocess.run(cmd, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError as exc:  # pragma: no cover - requires Godot
        raise SystemExit(f"Godot export failed with exit code {exc.returncode}.") from exc


def create_placeholder_bundle(export_name: str, output_dir: Path) -> None:
    scenes_dir = PROJECT_DIR / "scenes"
    output_dir.mkdir(parents=True, exist_ok=True)
    placeholder = output_dir / "index.html"
    placeholder.write_text(
        """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <title>KI Dev Tycoon – Placeholder Build</title>
    <style>body{font-family:system-ui;background:#10131a;color:#f1f5f9;padding:3rem;}code{background:#1e293b;padding:0.1rem 0.3rem;border-radius:4px;}</style>
  </head>
  <body>
    <h1>KI Dev Tycoon</h1>
    <p>Der echte {export_name}-Export wird erzeugt, sobald der Godot-CLI in der CI/CD-Pipeline verfügbar ist.</p>
    <p>Bis dahin enthält dieses Artefakt statische Szenen-Dateien als Referenz.</p>
  </body>
</html>
"""
    )
    scenes_snapshot = output_dir / "scenes.json"
    scenes_snapshot.write_text(
        json.dumps(
            sorted(str(p.relative_to(PROJECT_DIR)) for p in scenes_dir.rglob("*.tscn")),
        )
    )


def write_metadata(export_name: str, output_dir: Path, used_mock: bool) -> None:
    metadata = {
        "export": export_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "project_dir": str(PROJECT_DIR),
        "output_dir": str(output_dir),
        "mock": used_mock,
    }
    (output_dir / "build_metadata.json").write_text(json.dumps(metadata, indent=2))


def create_zip_archive(export_name: str, output_dir: Path) -> Path:
    archive_dir = DEFAULT_BUILD_DIR
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / ZIP_NAME_TEMPLATE.format(export=export_name)
    if archive_path.exists():
        archive_path.unlink()
    shutil.make_archive(str(archive_path.with_suffix("")), "zip", root_dir=output_dir)
    return archive_path


def main() -> None:
    args = parse_args()
    ensure_project_exists()

    output_dir = args.output or DEFAULT_BUILD_DIR / args.export
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    godot_available = shutil.which(str(args.godot_bin)) is not None
    used_mock = bool(args.mock_export or not godot_available)

    if not used_mock:
        exported = run_godot_export(args.godot_bin, args.export, output_dir)
        if not exported:
            print("Godot binary not found – falling back to placeholder export.")
            used_mock = True

    if used_mock:
        create_placeholder_bundle(args.export, output_dir)

    write_metadata(args.export, output_dir, used_mock)
    archive_path = create_zip_archive(args.export, output_dir)
    print(f"Artefacts written to {output_dir}")
    print(f"ZIP archive available at {archive_path}")


if __name__ == "__main__":
    main()
