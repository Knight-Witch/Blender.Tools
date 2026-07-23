#!/usr/bin/env python3
"""Restore and verify an isolated Blender add-on development source snapshot.

Usage:
    python tools/restore_dev_snapshot.py \
        addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_tree_digest(files: list[dict[str, Any]]) -> str:
    """Return the deterministic tree digest recorded by snapshot manifests."""
    digest = hashlib.sha256()
    for item in sorted(files, key=lambda value: value["path"]):
        digest.update(item["path"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(item["sha256"].encode("ascii"))
        digest.update(b"\0")
        digest.update(str(item["size"]).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def listed_parts(snapshot_dir: Path, manifest: dict[str, Any]) -> list[Path]:
    parts_dir = snapshot_dir / "parts"
    names = manifest.get("part_files")
    if names:
        paths = [parts_dir / str(name) for name in names]
    else:
        paths = sorted(parts_dir.glob("part_*.b64"))

    expected_parts = int(manifest["parts"])
    if len(paths) != expected_parts:
        raise RuntimeError(f"Expected {expected_parts} parts, found {len(paths)}")
    missing = [path.name for path in paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"Missing snapshot parts: {', '.join(missing)}")
    return paths


def verify_parts(part_paths: list[Path], manifest: dict[str, Any]) -> None:
    recorded = {
        item["file"]: item for item in manifest.get("part_manifest", [])
    }
    for path in part_paths:
        if not recorded:
            continue
        item = recorded.get(path.name)
        if item is None:
            raise RuntimeError(f"No manifest record for part: {path.name}")
        data = path.read_bytes()
        if len(data) != int(item["size"]):
            raise RuntimeError(
                f"Part size mismatch for {path.name}: expected {item['size']}, got {len(data)}"
            )
        actual = sha256_bytes(data)
        if actual != item["sha256"]:
            raise RuntimeError(
                f"Part SHA-256 mismatch for {path.name}: expected {item['sha256']}, got {actual}"
            )


def safe_extract(archive_path: Path, restored_dir: Path) -> None:
    with tarfile.open(archive_path, mode="r:xz") as archive:
        for member in archive.getmembers():
            path = PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts:
                raise RuntimeError(f"Unsafe archive path: {member.name}")
        archive.extractall(restored_dir, filter="data")


def verify_source_tree(restored_dir: Path, manifest: dict[str, Any]) -> None:
    package_root = restored_dir / manifest["package_root"]
    if not package_root.is_dir():
        raise RuntimeError(f"Missing package root: {manifest['package_root']}")

    actual_files: list[dict[str, Any]] = []
    for path in sorted(item for item in package_root.rglob("*") if item.is_file()):
        data = path.read_bytes()
        actual_files.append(
            {
                "path": path.relative_to(package_root).as_posix(),
                "size": len(data),
                "sha256": sha256_bytes(data),
            }
        )

    expected_tree = manifest.get("source_tree", {})
    if not expected_tree:
        return

    if len(actual_files) != int(expected_tree["file_count"]):
        raise RuntimeError(
            f"Source file-count mismatch: expected {expected_tree['file_count']}, got {len(actual_files)}"
        )
    actual_bytes = sum(item["size"] for item in actual_files)
    if actual_bytes != int(expected_tree["uncompressed_bytes"]):
        raise RuntimeError(
            "Source byte-count mismatch: "
            f"expected {expected_tree['uncompressed_bytes']}, got {actual_bytes}"
        )
    actual_tree_sha = source_tree_digest(actual_files)
    if actual_tree_sha != expected_tree["tree_sha256"]:
        raise RuntimeError(
            "Source tree SHA-256 mismatch: "
            f"expected {expected_tree['tree_sha256']}, got {actual_tree_sha}"
        )


def restore(snapshot_dir: Path) -> Path:
    manifest_path = snapshot_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    part_paths = listed_parts(snapshot_dir, manifest)
    verify_parts(part_paths, manifest)

    encoded = "".join(path.read_text(encoding="ascii").strip() for path in part_paths)
    archive_bytes = base64.b64decode(encoded, validate=True)
    actual_sha256 = sha256_bytes(archive_bytes)
    expected_sha256 = manifest["archive_sha256"]
    if actual_sha256 != expected_sha256:
        raise RuntimeError(
            f"Archive SHA-256 mismatch: expected {expected_sha256}, got {actual_sha256}"
        )
    if len(archive_bytes) != int(manifest["archive_size"]):
        raise RuntimeError(
            f"Archive size mismatch: expected {manifest['archive_size']}, got {len(archive_bytes)}"
        )

    archive_path = snapshot_dir / manifest["archive_name"]
    archive_path.write_bytes(archive_bytes)
    restored_dir = snapshot_dir / "restored"
    if restored_dir.exists():
        shutil.rmtree(restored_dir)
    restored_dir.mkdir(parents=True)
    safe_extract(archive_path, restored_dir)
    verify_source_tree(restored_dir, manifest)
    return restored_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir", type=Path)
    args = parser.parse_args()
    restored = restore(args.snapshot_dir.resolve())
    print(f"Restored and verified source at: {restored}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
