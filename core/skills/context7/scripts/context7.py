#!/usr/bin/env python3
"""Context7 API client for retrieving library documentation."""

import argparse
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://context7.com/api/v2"
MAX_RETRIES = 3
MAX_OUTPUT_CHARS = 30000


def get_api_key() -> str:
    """Get API key from environment."""
    key = os.environ.get("CONTEXT7_API_KEY")
    if not key:
        print("Error: CONTEXT7_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    if not key.startswith("ctx7sk"):
        print("Warning: API key should start with 'ctx7sk'", file=sys.stderr)
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


def output_response(content: str, prefix: str = "context7") -> None:
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


def make_request(endpoint: str, params: dict, retries: int = MAX_RETRIES) -> dict | str:
    """Make authenticated request to Context7 API with retry logic."""
    api_key = get_api_key()
    query_string = urllib.parse.urlencode(params)
    url = f"{BASE_URL}/{endpoint}?{query_string}"

    request = urllib.request.Request(url)
    request.add_header("Authorization", f"Bearer {api_key}")

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                content = response.read().decode("utf-8")
                content_type = response.headers.get("Content-Type", "")

                if "application/json" in content_type:
                    return json.loads(content)
                return content

        except urllib.error.HTTPError as e:
            # Handle retryable errors
            if e.code in (202, 429, 500, 503) and attempt < retries - 1:
                retry_after = e.headers.get("Retry-After")
                wait_time = int(retry_after) if retry_after else 2 ** attempt
                print(f"Retrying in {wait_time}s... (attempt {attempt + 1})", file=sys.stderr)
                time.sleep(wait_time)
                continue

            # Handle redirect
            if e.code == 301:
                try:
                    body = json.loads(e.read().decode("utf-8"))
                    new_id = body.get("redirectUrl", "")
                    print(f"Error: Library moved to {new_id}", file=sys.stderr)
                except Exception:
                    print("Error: Library redirected. Check response for new ID.", file=sys.stderr)
                sys.exit(1)

            error_messages = {
                202: "Library not finalized. Try again later.",
                400: "Bad request. Check parameters.",
                401: "Invalid API key. Verify CONTEXT7_API_KEY is correct (should start with ctx7sk).",
                403: "Access denied.",
                404: "Library not found. Use 'search' to find the correct library ID.",
                422: "Library too large or has no code snippets.",
                429: "Rate limit exceeded. Wait before retrying.",
                500: "Server error. Try again later.",
                503: "Service unavailable. Try again later.",
            }
            message = error_messages.get(e.code, f"HTTP {e.code}: {e.reason}")
            print(f"Error: {message}", file=sys.stderr)
            sys.exit(1)

        except urllib.error.URLError as e:
            print(f"Error: Network error - {e.reason}", file=sys.stderr)
            sys.exit(1)

    print("Error: Max retries exceeded", file=sys.stderr)
    sys.exit(1)


def search(args: argparse.Namespace) -> None:
    """Search for libraries by name."""
    params = {"libraryName": args.library, "query": args.query}
    result = make_request("libs/search", params)
    output = json.dumps(result, indent=2)
    output_response(output, "context7_search")


def docs(args: argparse.Namespace) -> None:
    """Get documentation for a library."""
    params = {"libraryId": args.library_id, "query": args.query}

    if args.format == "json":
        params["type"] = "json"
    else:
        params["type"] = "txt"

    result = make_request("context", params)

    if isinstance(result, str):
        output_response(result, "context7_docs")
    else:
        output = json.dumps(result, indent=2)
        output_response(output, "context7_docs")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Context7 API client for library documentation"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Search subcommand
    search_parser = subparsers.add_parser("search", help="Search for libraries")
    search_parser.add_argument(
        "--library", "-l", required=True, help="Library name to search for"
    )
    search_parser.add_argument(
        "--query", "-q", required=True, help="Query for relevance ranking"
    )
    search_parser.set_defaults(func=search)

    # Docs subcommand
    docs_parser = subparsers.add_parser("docs", help="Get library documentation")
    docs_parser.add_argument(
        "--library-id", "-l", required=True, help="Library ID (e.g., /facebook/react)"
    )
    docs_parser.add_argument(
        "--query", "-q", required=True, help="Documentation topic or question"
    )
    docs_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "txt"],
        default="txt",
        help="Output format (default: txt)",
    )
    docs_parser.set_defaults(func=docs)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
