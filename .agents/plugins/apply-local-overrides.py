#!/usr/bin/env python3
"""Apply local marketplace and plugin metadata overrides after upstream sync."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
DEFAULT_OVERRIDES = SCRIPT_DIR / "local-overrides.zh-CN.json"


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def merge_object(target: dict[str, Any], override: dict[str, Any]) -> None:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            merge_object(target[key], value)
        else:
            target[key] = value


def apply_file_override(path: Path, override: dict[str, Any]) -> bool:
    original = read_json(path)
    updated = json.loads(json.dumps(original))
    merge_object(updated, override)
    if updated == original:
        return False
    write_json(path, updated)
    return True


def apply_marketplace_overrides(overrides: dict[str, Any]) -> int:
    changed = 0
    for relative_path, override in overrides.get("marketplaces", {}).items():
        path = REPO_ROOT / relative_path
        if not path.exists():
            raise FileNotFoundError(f"Marketplace override target not found: {relative_path}")
        if apply_file_override(path, override):
            print(f"updated {relative_path}")
            changed += 1
    return changed


def apply_plugin_overrides(overrides: dict[str, Any]) -> int:
    changed = 0
    for plugin_name, override in overrides.get("plugins", {}).items():
        relative_path = Path("plugins") / plugin_name / ".codex-plugin" / "plugin.json"
        path = REPO_ROOT / relative_path
        if not path.exists():
            print(f"warning: plugin override target not found: {relative_path}")
            continue
        if apply_file_override(path, override):
            print(f"updated {relative_path}")
            changed += 1
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--overrides", type=Path, default=DEFAULT_OVERRIDES)
    args = parser.parse_args()

    overrides_path = args.overrides if args.overrides.is_absolute() else REPO_ROOT / args.overrides
    overrides = read_json(overrides_path)

    changed = 0
    changed += apply_marketplace_overrides(overrides)
    changed += apply_plugin_overrides(overrides)
    print(f"applied local overrides; changed {changed} file(s)")


if __name__ == "__main__":
    main()
