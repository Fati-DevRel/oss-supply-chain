#!/usr/bin/env python3
"""
URL Extractor and Validator for Book Manuscripts

This script extracts all URLs from markdown files in the book repository
and verifies that they are still valid (return HTTP 200 or redirect to valid pages).

Usage:
    python3 verify_urls.py [--output report.json] [--timeout 10] [--workers 10]
"""

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests
from requests.exceptions import RequestException


@dataclass
class URLInfo:
    """Information about a URL found in the book."""
    url: str
    file_path: str
    line_number: int
    context: str = ""  # Surrounding text for context


@dataclass
class ValidationResult:
    """Result of validating a URL."""
    url: str
    status: str  # "valid", "invalid", "redirect", "timeout", "error"
    status_code: Optional[int] = None
    final_url: Optional[str] = None
    error_message: Optional[str] = None
    response_time_ms: Optional[float] = None
    occurrences: list = field(default_factory=list)


def find_markdown_files(root_dir: str) -> list[Path]:
    """Find all markdown files in the repository."""
    root = Path(root_dir)
    md_files = []

    for pattern in ["**/*.md"]:
        md_files.extend(root.glob(pattern))

    return sorted(md_files)


def extract_urls_from_file(file_path: Path) -> list[URLInfo]:
    """Extract all URLs from a markdown file."""
    urls = []

    # Regex pattern for URLs - handles various markdown formats
    # Matches: http(s)://... stopping at whitespace, ), ], >, or "
    url_pattern = re.compile(
        r'https?://[^\s\)\]\>"\'`<]+[^\s\)\]\>"\'`<.,;:!?\-]'
    )

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        for line_num, line in enumerate(lines, start=1):
            matches = url_pattern.findall(line)
            for url in matches:
                # Clean up any trailing punctuation that might have slipped through
                url = url.rstrip('.,;:!?')

                # Get context (the line containing the URL)
                context = line.strip()[:200]  # Limit context length

                urls.append(URLInfo(
                    url=url,
                    file_path=str(file_path),
                    line_number=line_num,
                    context=context
                ))
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)

    return urls


def validate_url(url: str, timeout: int = 10) -> ValidationResult:
    """Validate a single URL by making an HTTP HEAD/GET request."""
    result = ValidationResult(url=url, status="unknown")

    # Skip certain URLs that are known to be problematic or are examples
    skip_patterns = [
        "example.com",
        "example.org",
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "internal",
        "your-",
        "my-",
        "<",
        ">",
        "${",
        "{{",
        "[IP",
        "attacker.example.com",
        "cdn.example.com",
        "trusted-cdn.example.com"
        "cdn.polyfill.io",
        "token.actions.githubusercontent.com"
    ]

    if any(pattern in url.lower() for pattern in skip_patterns):
        result.status = "skipped"
        result.error_message = "Example/placeholder URL"
        return result

    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; BookURLValidator/1.0; +https://github.com)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    start_time = time.time()

    try:
        # Try HEAD first (faster, less bandwidth)
        response = requests.head(
            url,
            timeout=timeout,
            headers=headers,
            allow_redirects=True
        )

        # Some servers don't support HEAD, fall back to GET
        if response.status_code >= 400:
            response = requests.get(
                url,
                timeout=timeout,
                headers=headers,
                allow_redirects=True,
                stream=True  # Don't download body
            )
            response.close()

        elapsed_ms = (time.time() - start_time) * 1000
        result.status_code = response.status_code
        result.response_time_ms = round(elapsed_ms, 2)
        result.final_url = response.url if response.url != url else None

        if response.status_code == 200:
            result.status = "valid"
        elif 300 <= response.status_code < 400:
            result.status = "redirect"
        elif response.status_code == 403:
            # Many sites block automated requests but are still valid
            result.status = "blocked"
            result.error_message = "Request blocked (403 Forbidden) - URL may still be valid"
        elif response.status_code == 404:
            result.status = "not_found"
            result.error_message = "Page not found (404)"
        elif response.status_code == 429:
            result.status = "rate_limited"
            result.error_message = "Rate limited - try again later"
        else:
            result.status = "invalid"
            result.error_message = f"HTTP {response.status_code}"

    except requests.exceptions.Timeout:
        result.status = "timeout"
        result.error_message = f"Request timed out after {timeout}s"
    except requests.exceptions.SSLError as e:
        result.status = "ssl_error"
        result.error_message = f"SSL/TLS error: {str(e)[:100]}"
    except requests.exceptions.ConnectionError as e:
        result.status = "connection_error"
        result.error_message = f"Connection failed: {str(e)[:100]}"
    except RequestException as e:
        result.status = "error"
        result.error_message = str(e)[:200]
    except Exception as e:
        result.status = "error"
        result.error_message = f"Unexpected error: {str(e)[:100]}"

    return result


def validate_urls_parallel(
    urls: dict[str, list[URLInfo]],
    timeout: int = 10,
    max_workers: int = 10,
    progress_callback=None
) -> dict[str, ValidationResult]:
    """Validate multiple URLs in parallel."""
    results = {}
    total = len(urls)
    completed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(validate_url, url, timeout): url
            for url in urls.keys()
        }

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                result.occurrences = [asdict(info) for info in urls[url]]
                results[url] = result
            except Exception as e:
                results[url] = ValidationResult(
                    url=url,
                    status="error",
                    error_message=str(e),
                    occurrences=[asdict(info) for info in urls[url]]
                )

            completed += 1
            if progress_callback:
                progress_callback(completed, total, url, results[url])

    return results


def print_progress(completed: int, total: int, url: str, result: ValidationResult):
    """Print progress during validation."""
    status_symbols = {
        "valid": "✓",
        "skipped": "⊘",
        "redirect": "→",
        "blocked": "⚠",
        "not_found": "✗",
        "invalid": "✗",
        "timeout": "⏱",
        "ssl_error": "🔒",
        "connection_error": "⚡",
        "rate_limited": "⏳",
        "error": "!",
    }
    symbol = status_symbols.get(result.status, "?")

    # Truncate URL for display
    display_url = url[:70] + "..." if len(url) > 73 else url

    print(f"[{completed:4d}/{total:4d}] {symbol} {display_url}")


def generate_report(
    results: dict[str, ValidationResult],
    output_format: str = "text"
) -> str:
    """Generate a report of the validation results."""

    # Categorize results
    categories = {
        "valid": [],
        "skipped": [],
        "redirect": [],
        "blocked": [],
        "not_found": [],
        "invalid": [],
        "timeout": [],
        "ssl_error": [],
        "connection_error": [],
        "rate_limited": [],
        "error": [],
    }

    for url, result in results.items():
        status = result.status
        if status in categories:
            categories[status].append(result)
        else:
            categories["error"].append(result)

    if output_format == "json":
        return json.dumps({
            "summary": {
                "total": len(results),
                "valid": len(categories["valid"]),
                "skipped": len(categories["skipped"]),
                "problematic": sum(len(categories[k]) for k in
                    ["not_found", "invalid", "timeout", "ssl_error",
                     "connection_error", "error"]),
            },
            "results": {url: asdict(r) for url, r in results.items()}
        }, indent=2)

    # Text report
    lines = []
    lines.append("=" * 80)
    lines.append("URL VALIDATION REPORT")
    lines.append("=" * 80)
    lines.append("")

    # Summary
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total unique URLs:    {len(results)}")
    lines.append(f"Valid:                {len(categories['valid'])}")
    lines.append(f"Skipped (examples):   {len(categories['skipped'])}")
    lines.append(f"Redirects:            {len(categories['redirect'])}")
    lines.append(f"Blocked (403):        {len(categories['blocked'])}")
    lines.append(f"Not Found (404):      {len(categories['not_found'])}")
    lines.append(f"Timeouts:             {len(categories['timeout'])}")
    lines.append(f"SSL Errors:           {len(categories['ssl_error'])}")
    lines.append(f"Connection Errors:    {len(categories['connection_error'])}")
    lines.append(f"Rate Limited:         {len(categories['rate_limited'])}")
    lines.append(f"Other Errors:         {len(categories['error']) + len(categories['invalid'])}")
    lines.append("")

    # Problem URLs
    problem_categories = [
        ("NOT FOUND (404)", "not_found"),
        ("INVALID RESPONSES", "invalid"),
        ("TIMEOUTS", "timeout"),
        ("SSL ERRORS", "ssl_error"),
        ("CONNECTION ERRORS", "connection_error"),
        ("OTHER ERRORS", "error"),
    ]

    for title, category in problem_categories:
        if categories[category]:
            lines.append("")
            lines.append(f"{title}")
            lines.append("-" * 40)
            for result in sorted(categories[category], key=lambda r: r.url):
                lines.append(f"  URL: {result.url}")
                if result.error_message:
                    lines.append(f"  Error: {result.error_message}")
                if result.occurrences:
                    lines.append(f"  Found in:")
                    for occ in result.occurrences[:3]:  # Limit to 3 occurrences
                        lines.append(f"    - {occ['file_path']}:{occ['line_number']}")
                    if len(result.occurrences) > 3:
                        lines.append(f"    ... and {len(result.occurrences) - 3} more locations")
                lines.append("")

    # Redirects (informational)
    if categories["redirect"]:
        lines.append("")
        lines.append("REDIRECTS (informational)")
        lines.append("-" * 40)
        for result in sorted(categories["redirect"], key=lambda r: r.url)[:20]:
            lines.append(f"  {result.url}")
            lines.append(f"    → {result.final_url}")
        if len(categories["redirect"]) > 20:
            lines.append(f"  ... and {len(categories['redirect']) - 20} more redirects")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract and validate URLs from book markdown files"
    )
    parser.add_argument(
        "--root", "-r",
        default=".",
        help="Root directory of the book repository (default: current directory)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for the report (default: stdout)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)"
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=10,
        help="Number of parallel workers (default: 10)"
    )
    parser.add_argument(
        "--extract-only",
        action="store_true",
        help="Only extract URLs, don't validate them"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )

    args = parser.parse_args()

    # Find all markdown files
    print(f"Scanning for markdown files in {args.root}...", file=sys.stderr)
    md_files = find_markdown_files(args.root)
    print(f"Found {len(md_files)} markdown files", file=sys.stderr)

    # Extract URLs from all files
    print("Extracting URLs...", file=sys.stderr)
    all_url_infos = []
    for md_file in md_files:
        all_url_infos.extend(extract_urls_from_file(md_file))

    # Deduplicate URLs while keeping track of all occurrences
    url_occurrences: dict[str, list[URLInfo]] = {}
    for info in all_url_infos:
        if info.url not in url_occurrences:
            url_occurrences[info.url] = []
        url_occurrences[info.url].append(info)

    print(f"Found {len(all_url_infos)} URL references ({len(url_occurrences)} unique URLs)", file=sys.stderr)

    if args.extract_only:
        # Just output the extracted URLs
        for url, occurrences in sorted(url_occurrences.items()):
            print(f"{url}")
            for occ in occurrences:
                print(f"  - {occ.file_path}:{occ.line_number}")
        return

    # Validate URLs
    print(f"\nValidating URLs with {args.workers} workers (timeout: {args.timeout}s)...", file=sys.stderr)
    print("", file=sys.stderr)

    progress_fn = None if args.quiet else print_progress
    results = validate_urls_parallel(
        url_occurrences,
        timeout=args.timeout,
        max_workers=args.workers,
        progress_callback=progress_fn
    )

    # Generate report
    report = generate_report(results, args.format)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\nReport written to {args.output}", file=sys.stderr)
    else:
        print("\n")
        print(report)


if __name__ == "__main__":
    main()
