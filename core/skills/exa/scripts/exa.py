#!/usr/bin/env python3
"""Exa API client for web search and content extraction."""

import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request

BASE_URL = "https://api.exa.ai"
MAX_OUTPUT_CHARS = 30000


def get_api_key() -> str:
    """Get API key from environment."""
    key = os.environ.get("EXA_API_KEY")
    if not key:
        print("Error: EXA_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    return key


def analyze_content(content: str) -> dict:
    """Analyze content for file summary."""
    lines = content.split("\n")
    line_lengths = [len(line) for line in lines]
    return {
        "lines": len(lines),
        "chars": len(content),
        "max_line_chars": max(line_lengths) if line_lengths else 0,
    }


def output_response(content: str, prefix: str = "exa") -> None:
    """Output response, writing to temp file if too long."""
    if len(content) <= MAX_OUTPUT_CHARS:
        print(content)
        return

    # Write to temp file
    stats = analyze_content(content)
    fd, path = tempfile.mkstemp(prefix=f"{prefix}_", suffix=".txt")
    with os.fdopen(fd, "w") as f:
        f.write(content)

    print(f"Response too long, saved to file:", file=sys.stderr)
    print(f"  Path: {path}", file=sys.stderr)
    print(f"  Lines: {stats['lines']}", file=sys.stderr)
    print(f"  Characters: {stats['chars']}", file=sys.stderr)
    print(f"  Max line length: {stats['max_line_chars']}", file=sys.stderr)


def make_request(endpoint: str, data: dict) -> dict:
    """Make authenticated POST request to Exa API."""
    api_key = get_api_key()
    url = f"{BASE_URL}/{endpoint}"

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "User-Agent": "exa-cli/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as e:
        error_messages = {
            400: "Bad request. Check query parameters.",
            401: "Invalid API key. Verify EXA_API_KEY is correct.",
            429: "Rate limit exceeded.",
            500: "Server error. Try again later.",
        }
        message = error_messages.get(e.code, f"HTTP {e.code}: {e.reason}")
        print(f"Error: {message}", file=sys.stderr)
        sys.exit(1)

    except urllib.error.URLError as e:
        print(f"Error: Network error - {e.reason}", file=sys.stderr)
        sys.exit(1)


def format_search_results(results: list) -> str:
    """Format search results as text."""
    if not results:
        return "No results found"

    output = []
    for r in results:
        output.append(f"## {r.get('title', 'Untitled')}")
        output.append(f"URL: {r.get('url', '')}")
        if r.get("publishedDate"):
            output.append(f"Date: {r.get('publishedDate')}")
        text = r.get("text", "")
        if text:
            output.append(f"\n{text}")
        output.append("")
    return "\n".join(output)


def search(args: argparse.Namespace) -> None:
    """Search the web using Exa."""
    data = {
        "query": args.query,
        "type": args.type,
        "numResults": args.num_results,
    }

    if args.text:
        data["text"] = True

    if args.context:
        data["context"] = True

    if args.include_domains:
        data["includeDomains"] = args.include_domains.split(",")

    if args.exclude_domains:
        data["excludeDomains"] = args.exclude_domains.split(",")

    if args.start_date:
        data["startPublishedDate"] = args.start_date

    if args.end_date:
        data["endPublishedDate"] = args.end_date

    result = make_request("search", data)

    if args.format == "json":
        output = json.dumps(result, indent=2)
    else:
        output = format_search_results(result.get("results", []))

    output_response(output, "exa_search")


def contents(args: argparse.Namespace) -> None:
    """Extract content from specific URLs."""
    data = {
        "urls": args.urls.split(","),
        "text": True,
    }

    if args.livecrawl:
        data["livecrawl"] = args.livecrawl

    result = make_request("contents", data)

    if args.format == "json":
        output = json.dumps(result, indent=2)
    else:
        results = result.get("results", [])
        if not results:
            output = "No content extracted"
        else:
            parts = []
            for r in results:
                parts.append(f"## {r.get('title', 'Untitled')}")
                parts.append(f"URL: {r.get('url', '')}")
                text = r.get("text", "")
                if text:
                    parts.append(f"\n{text}")
                parts.append("")
            output = "\n".join(parts)

    output_response(output, "exa_contents")


def code(args: argparse.Namespace) -> None:
    """Find code examples and programming context."""
    data = {
        "query": args.query,
    }

    if args.tokens:
        if args.tokens == "dynamic":
            data["tokensNum"] = "dynamic"
        else:
            data["tokensNum"] = int(args.tokens)

    result = make_request("context", data)

    if args.format == "json":
        output = json.dumps(result, indent=2)
    else:
        response = result.get("response", "")
        if not response:
            output = "No code examples found"
        else:
            count = result.get("resultsCount", 0)
            tokens = result.get("outputTokens", 0)
            footer = f"\n---\nSources: {count} | Tokens: {tokens}" if count or tokens else ""
            output = response + footer

    output_response(output, "exa_code")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exa API client for web search and content extraction"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Search subcommand
    search_parser = subparsers.add_parser("search", help="Search the web")
    search_parser.add_argument(
        "--query", "-q", required=True, help="Search query"
    )
    search_parser.add_argument(
        "--type",
        "-t",
        choices=["fast", "auto", "deep"],
        default="auto",
        help="Search type: fast, auto (default), or deep",
    )
    search_parser.add_argument(
        "--num-results",
        "-n",
        type=int,
        default=10,
        help="Number of results (default: 10, max: 100)",
    )
    search_parser.add_argument(
        "--text", action="store_true", help="Include full text content"
    )
    search_parser.add_argument(
        "--context", action="store_true", help="Include LLM-optimized context"
    )
    search_parser.add_argument(
        "--include-domains", help="Comma-separated domains to include"
    )
    search_parser.add_argument(
        "--exclude-domains", help="Comma-separated domains to exclude"
    )
    search_parser.add_argument(
        "--start-date", help="Filter from date (ISO 8601)"
    )
    search_parser.add_argument(
        "--end-date", help="Filter to date (ISO 8601)"
    )
    search_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    search_parser.set_defaults(func=search)

    # Contents subcommand
    contents_parser = subparsers.add_parser(
        "contents", help="Extract content from URLs"
    )
    contents_parser.add_argument(
        "--urls", "-u", required=True, help="Comma-separated URLs to extract"
    )
    contents_parser.add_argument(
        "--livecrawl",
        choices=["never", "fallback", "preferred", "always"],
        help="Live crawl mode",
    )
    contents_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    contents_parser.set_defaults(func=contents)

    # Code subcommand
    code_parser = subparsers.add_parser(
        "code", help="Find code examples and programming context"
    )
    code_parser.add_argument(
        "--query", "-q", required=True, help="Programming query"
    )
    code_parser.add_argument(
        "--tokens",
        "-t",
        default="5000",
        help="Token limit: 'dynamic' or 50-100000 (default: 5000)",
    )
    code_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    code_parser.set_defaults(func=code)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
