#!/usr/bin/env python3
"""Restore an isolated Blender add-on development source snapshot.

Usage:
    python tools/restore_dev_snapshot.py addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import tarfile
from pathlib import Path


def restore(snapshot_dir: Path) -> Path:
    manifest_path = snapshot_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    parts_dir = snapshot_dir / "parts"
    part_paths = sorted(parts_dir.glob("part_*.b64"))
    expected_parts = int(manifest["parts"])
    if len(part_paths) != expected_parts:
        raise RuntimeError(f"Expected {expected_parts} parts, found {len(part_paths)}")

    encoded = "".join(path.read_text(encoding="ascii").strip() for path in part_paths)
    archive_bytes = base64.b64decode(encoded, validate=True)
    actual_sha256 = hashlib.sha256(archive_bytes).hexdigest()
    expected_sha256 = manifest["archive_sha256"]
    if actual_sha256 != expected_sha256:
        raise RuntimeError(
            f"SHA-256 mismatch: expected {expected_sha256}, got {actual_sha256}"
        )

    archive_path = snapshot_dir / manifest["archive_name"]
    archive_path.write_bytes(archive_bytes)
    restored_dir = snapshot_dir / "restored"
    if restored_dir.exists():
        shutil.rmtree(restored_dir)
    restored_dir.mkdir(parents=True)
    with tarfile.open(archive_path, mode="r:xz") as archive:
        archive.extractall(restored_dir, filter="data")
    return restored_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir", type=Path)
    args = parser.parse_args()
    restored = restore(args.snapshot_dir.resolve())
    print(f"Restored source to: {restored}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
