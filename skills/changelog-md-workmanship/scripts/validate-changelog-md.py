#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


GENERIC_PHRASES = [
    "many improvements",
    "various fixes",
    "misc changes",
    "and more",
    "several updates",
]


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def in_git_repo(path: Path) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=path.parent,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def git_tags(path: Path) -> list[str]:
    result = subprocess.run(
        ["git", "tag"],
        cwd=path.parent,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def verify_http_links(urls: list[str], report: Report, timeout: float) -> None:
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", "changelog-md-workmanship-validator/1.0")]

    for url in urls:
        try:
            request = urllib.request.Request(url, method="HEAD")
            with opener.open(request, timeout=timeout) as response:
                status = getattr(response, "status", response.getcode())
            if status >= 400:
                report.warn(f"Link returned HTTP {status}: {url}")
                continue
        except urllib.error.HTTPError as error:
            if error.code == 405:
                try:
                    request = urllib.request.Request(url, method="GET")
                    with opener.open(request, timeout=timeout) as response:
                        status = getattr(response, "status", response.getcode())
                    if status >= 400:
                        report.warn(f"Link returned HTTP {status}: {url}")
                except urllib.error.URLError as inner_error:
                    report.warn(f"Link verification failed for {url}: {inner_error.reason}")
                except urllib.error.HTTPError as inner_error:
                    report.warn(f"Link returned HTTP {inner_error.code}: {url}")
            else:
                report.warn(f"Link returned HTTP {error.code}: {url}")
        except urllib.error.URLError as error:
            report.warn(f"Link verification failed for {url}: {error.reason}")


def validate_with_options(
    content: str,
    path: Path,
    *,
    verify_links: bool,
    max_links: int,
    timeout: float,
) -> Report:
    report = Report()

    if "Scope window:" not in content:
        report.error("Missing explicit `Scope window:` line")

    if not re.search(r"^## (Version|Release) Timeline\b", content, flags=re.MULTILINE):
        report.error("Missing `Version Timeline` or `Release Timeline` section")

    if "Representative commits" not in content:
        report.error("Missing `Representative commits` section")

    if "Delivered capability" not in content:
        report.warn("Missing `Delivered capability` sections")

    commit_urls = re.findall(r"https://github\.com/[^)\s]+/commit/[0-9a-fA-F]{7,40}", content)
    if not commit_urls:
        report.error("No live GitHub commit URLs found")

    content_without_markdown_links = re.sub(r"\[[^\]]*\]\([^)]+\)", "", content)
    bare_shas = set(
        re.findall(
            r"(?<!/commit/)(?<![0-9a-fA-F])[0-9a-fA-F]{7,40}(?![0-9a-fA-F])",
            content_without_markdown_links,
        )
    )
    if bare_shas:
        report.warn(
            f"Found possible bare commit hashes not wrapped in live links: {', '.join(sorted(list(bare_shas))[:8])}"
        )

    if not re.search(r"https://github\.com/[^)\s]+/(releases/tag|tree)/", content):
        report.warn("No GitHub release/tag URLs found in the version timeline")

    if "Closed workstreams" not in content and "Completed workstreams" not in content:
        report.warn("No workstream section found; tracker intent may be missing")

    lowered = content.lower()
    for phrase in GENERIC_PHRASES:
        if phrase in lowered:
            report.warn(f"Contains low-signal phrase: `{phrase}`")

    if in_git_repo(path):
        tags = git_tags(path)
        if tags and not any(tag in content for tag in tags[: min(10, len(tags))]):
            report.warn("Git tags exist locally, but none of the first tags appeared in the changelog")

    if verify_links:
        markdown_urls = list(
            dict.fromkeys(re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", content))
        )
        if not markdown_urls:
            report.warn("Link verification requested, but no markdown HTTP(S) links were found")
        else:
            verify_http_links(markdown_urls[:max_links], report, timeout)
            if len(markdown_urls) > max_links:
                report.warn(
                    f"Verified only the first {max_links} markdown links out of {len(markdown_urls)} total links"
                )

    return report


def validate(content: str, path: Path) -> Report:
    return validate_with_options(
        content,
        path,
        verify_links=False,
        max_links=0,
        timeout=0.0,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a CHANGELOG.md file")
    parser.add_argument("path", help="Path to CHANGELOG.md")
    parser.add_argument(
        "--verify-links",
        action="store_true",
        help="Perform live HTTP verification of markdown links",
    )
    parser.add_argument(
        "--max-links",
        type=int,
        default=25,
        help="Maximum number of markdown links to verify when --verify-links is enabled",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Per-request timeout in seconds for live link verification",
    )
    args = parser.parse_args()

    path = Path(args.path).resolve()
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 1

    report = validate_with_options(
        path.read_text(),
        path,
        verify_links=args.verify_links,
        max_links=max(args.max_links, 0),
        timeout=max(args.timeout, 0.1),
    )

    print("=" * 60)
    print(f"Changelog Validation Report: {path.name}")
    print("=" * 60)

    if report.errors:
        print(f"\n[ERRORS] {len(report.errors)} issue(s) found:")
        for msg in report.errors:
            print(f"  ✗ {msg}")

    if report.warnings:
        print(f"\n[WARNINGS] {len(report.warnings)} suggestion(s):")
        for msg in report.warnings:
            print(f"  ⚠ {msg}")

    if not report.errors and not report.warnings:
        print("\n✓ Changelog looks strong!")
    elif not report.errors:
        print("\n✓ Changelog passes structural checks (with warnings)")
    else:
        print("\n✗ Changelog needs fixes")

    print()
    return 0 if not report.errors else 1


if __name__ == "__main__":
    sys.exit(main())
