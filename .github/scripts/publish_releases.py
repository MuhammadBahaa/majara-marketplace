#!/usr/bin/env python3
"""Publish a GitHub Release for every plugin version not yet released here.

Runs inside the generated distribution repo, where .claude-plugin/marketplace.json
is the list of published plugins and their versions. For each entry it creates
the tag <plugin>/v<version> -- matching the Majarrah Cubiq release-tag convention --
with the matching CHANGELOG section as the release notes. Existing releases are
left untouched, so re-running is safe and a plugin-less release is a no-op.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def published_plugins() -> list:
    marketplace = json.loads(
        (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    return [
        (entry["name"], entry["version"])
        for entry in marketplace.get("plugins", [])
        if entry.get("name") and entry.get("version")
    ]


def changelog_section(name: str, version: str) -> str:
    """The CHANGELOG block for one version, or a bare fallback line."""
    changelog = ROOT / "plugins" / name / "CHANGELOG.md"
    if changelog.is_file():
        match = re.search(
            rf"^## {re.escape(version)}\b.*?(?=^## |\Z)",
            changelog.read_text(encoding="utf-8"),
            re.MULTILINE | re.DOTALL,
        )
        if match:
            return match.group(0).strip()
    return f"{name} {version}"


def release_exists(tag: str) -> bool:
    return subprocess.run(
        ["gh", "release", "view", tag],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def create_release(name: str, version: str, tag: str) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as notes:
        notes.write(changelog_section(name, version) + "\n")
        notes_path = notes.name
    subprocess.run(
        ["gh", "release", "create", tag,
         "--title", f"{name} {version}",
         "--notes-file", notes_path],
        check=True,
    )


def main() -> int:
    plugins = published_plugins()
    if not plugins:
        print("no published plugins in marketplace.json - nothing to release")
        return 0
    for name, version in plugins:
        tag = f"{name}/v{version}"
        if release_exists(tag):
            print(f"release {tag} already published - skipping")
            continue
        create_release(name, version, tag)
        print(f"published release {tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
