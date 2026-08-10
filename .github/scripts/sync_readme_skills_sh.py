#!/usr/bin/env python3
"""Regenerate the skills.sh-facing parts of README.md from the repo's own contents.

skills.sh has no publish or refresh API -- it crawls the public repo on its own
schedule -- so the only thing a release can keep correct is what this repo says
about skills.sh. Two spots drift whenever a skill is added, renamed, or dropped:

  * the install-count badge, which encodes the owner/repo slug, and
  * the "Every skill also has its own page on skills.sh:" link list.

Both are rebuilt here from .claude-plugin/marketplace.json (plugin order) and the
SKILL.md frontmatter under plugins/*/skills/*/ (skill names). The Plugins table is
deliberately left alone: its prose is hand-written, not derived from any manifest.

Anchors are matched by content rather than by injected markers, so the script keeps
working against a README regenerated upstream in MajarrahCore. Anything it cannot
find is reported and skipped -- a README that has moved on is not a release failure.

Exit codes: 0 = README already correct, 0 = rewritten (see --check), 1 = drift found
under --check.

NOTE: this file lives only in the distribution repo. A republish from MajarrahCore
overwrites .github/, so port it to distribution/majarrah-marketplace/ to keep it.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

SENTINEL = "Every skill also has its own page on skills.sh:"
BADGE_RE = re.compile(r"\[!\[skills\.sh installs\]\([^)]*\)\]\([^)]*\)")


def repo_slug() -> tuple[str, str]:
    """(owner, repo) from the Actions env, falling back to the git remote."""
    import os

    env = os.environ.get("GITHUB_REPOSITORY", "")
    if "/" in env:
        owner, _, repo = env.partition("/")
        return owner, repo
    url = subprocess.run(
        ["git", "-C", str(ROOT), "remote", "get-url", "origin"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    match = re.search(r"[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
    if not match:
        raise SystemExit(f"cannot parse owner/repo from remote {url!r}")
    return match.group(1), match.group(2)


def frontmatter_name(skill: Path) -> str:
    """The `name:` from a SKILL.md's frontmatter, or the directory name."""
    text = skill.read_text(encoding="utf-8")
    if text.startswith("---"):
        _, _, rest = text.partition("\n")
        block, _, _ = rest.partition("\n---")
        for line in block.splitlines():
            key, sep, value = line.partition(":")
            if sep and key == "name":
                return value.strip().strip("\"'")
    return skill.parent.name


def plugin_order() -> list[str]:
    marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    return [p["name"] for p in marketplace.get("plugins", []) if p.get("name")]


def discovered_skills() -> list[str]:
    """Skill names in marketplace plugin order, alphabetical within a plugin.

    Plugins present on disk but absent from marketplace.json are appended last, so
    a skill is never silently dropped from the README just because the manifest
    has not caught up yet.
    """
    ordered = plugin_order()
    by_plugin: dict[str, list[str]] = {}
    for skill in sorted((ROOT / "plugins").glob("*/skills/*/SKILL.md")):
        plugin = skill.parents[2].name
        by_plugin.setdefault(plugin, []).append(frontmatter_name(skill))
    names: list[str] = []
    for plugin in ordered + [p for p in sorted(by_plugin) if p not in ordered]:
        names.extend(sorted(by_plugin.get(plugin, [])))
    return names


def badge_line(owner: str, repo: str) -> str:
    return (
        f"[![skills.sh installs](https://skills.sh/b/{owner}/{repo})]"
        f"(https://skills.sh/{owner}/{repo})"
    )


def links_block(owner: str, repo: str, skills: list[str]) -> str:
    base = f"https://skills.sh/{owner.lower()}/{repo.lower()}"
    links = [f"[`{name}`]({base}/{name})" for name in skills]
    return SENTINEL + "\n" + " ·\n".join(links)


def replace_links_block(text: str, block: str) -> tuple[str, bool]:
    """Swap the sentinel paragraph for `block`; False if the sentinel is gone."""
    start = text.find(SENTINEL)
    if start == -1:
        return text, False
    end = text.find("\n\n", start)
    end = len(text) if end == -1 else end
    return text[:start] + block + text[end:], True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true",
        help="report drift and exit 1 instead of rewriting README.md",
    )
    args = parser.parse_args()

    owner, repo = repo_slug()
    skills = discovered_skills()
    if not skills:
        print("no SKILL.md files found under plugins/ - leaving README.md alone")
        return 0

    original = README.read_text(encoding="utf-8")
    updated, count = BADGE_RE.subn(badge_line(owner, repo), original)
    if not count:
        print("warning: skills.sh install badge not found - skipping badge sync")
    updated, found = replace_links_block(updated, links_block(owner, repo, skills))
    if not found:
        print(f"warning: {SENTINEL!r} not found - skipping skill link sync")

    if not count and not found:
        print("no skills.sh sections found in README.md - nothing to sync")
        return 0
    if updated == original:
        print(f"README.md skills.sh sections already current ({len(skills)} skills)")
        return 0
    if args.check:
        print("README.md skills.sh sections are out of date")
        return 1
    README.write_text(updated, encoding="utf-8")
    print(f"README.md skills.sh sections updated: {', '.join(skills)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
