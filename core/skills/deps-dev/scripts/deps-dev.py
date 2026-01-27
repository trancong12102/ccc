#!/usr/bin/env python3
"""deps.dev API client for looking up package versions."""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://api.deps.dev/v3"

SYSTEMS = {
    "npm": "NPM",
    "pypi": "PYPI",
    "go": "GO",
    "cargo": "CARGO",
    "maven": "MAVEN",
    "nuget": "NUGET",
    "rubygems": "RUBYGEMS",
}


def make_request(path: str) -> dict:
    """Make request to deps.dev API."""
    url = f"{BASE_URL}/{path}"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as e:
        error_messages = {
            400: "Bad request. Check package name and system.",
            404: "Package not found. Check spelling and ecosystem.",
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


def normalize_system(system: str) -> str:
    """Normalize system name to API format."""
    lower = system.lower()
    if lower in SYSTEMS:
        return SYSTEMS[lower]
    # Already uppercase format
    if system.upper() in SYSTEMS.values():
        return system.upper()
    print(f"Error: Unknown system '{system}'", file=sys.stderr)
    print(f"Supported systems: {', '.join(SYSTEMS.keys())}", file=sys.stderr)
    sys.exit(1)


def encode_package_name(name: str) -> str:
    """URL-encode package name for API request."""
    return urllib.parse.quote(name, safe="")


def get_package(args: argparse.Namespace) -> None:
    """Get package info including all versions."""
    system = normalize_system(args.system)
    encoded_name = encode_package_name(args.package)
    path = f"systems/{system}/packages/{encoded_name}"

    result = make_request(path)

    # Find default version
    default_version = None
    for version in result.get("versions", []):
        if version.get("isDefault"):
            default_version = version.get("versionKey", {}).get("version")
            break

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        name = result.get("packageKey", {}).get("name", args.package)
        print(f"Package: {name}")
        print(f"System: {system}")
        if default_version:
            print(f"Latest: {default_version}")
        else:
            print("Latest: (no default version found)")

        if args.all_versions:
            print("\nVersions:")
            for v in result.get("versions", [])[-10:]:
                vk = v.get("versionKey", {})
                version = vk.get("version", "unknown")
                is_default = " (default)" if v.get("isDefault") else ""
                print(f"  {version}{is_default}")


def get_version(args: argparse.Namespace) -> None:
    """Get specific version details."""
    system = normalize_system(args.system)
    encoded_name = encode_package_name(args.package)
    encoded_version = encode_package_name(args.version)
    path = f"systems/{system}/packages/{encoded_name}/versions/{encoded_version}"

    result = make_request(path)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        vk = result.get("versionKey", {})
        print(f"Package: {vk.get('name', args.package)}")
        print(f"Version: {vk.get('version', args.version)}")
        print(f"System: {system}")
        print(f"Published: {result.get('publishedAt', 'unknown')}")
        print(f"Default: {result.get('isDefault', False)}")

        licenses = result.get("licenses", [])
        if licenses:
            print(f"Licenses: {', '.join(licenses)}")

        advisories = result.get("advisoryKeys", [])
        if advisories:
            print(f"Advisories: {len(advisories)} security advisory(ies)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="deps.dev API client for package version lookup"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Package subcommand
    pkg_parser = subparsers.add_parser("package", help="Get package info")
    pkg_parser.add_argument(
        "--system", "-s", required=True, help="Package ecosystem (npm, pypi, go, etc.)"
    )
    pkg_parser.add_argument("--package", "-p", required=True, help="Package name")
    pkg_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    pkg_parser.add_argument(
        "--all-versions", "-a", action="store_true", help="Show recent versions"
    )
    pkg_parser.set_defaults(func=get_package)

    # Version subcommand
    ver_parser = subparsers.add_parser("version", help="Get specific version details")
    ver_parser.add_argument(
        "--system", "-s", required=True, help="Package ecosystem (npm, pypi, go, etc.)"
    )
    ver_parser.add_argument("--package", "-p", required=True, help="Package name")
    ver_parser.add_argument("--version", "-v", required=True, help="Version number")
    ver_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    ver_parser.set_defaults(func=get_version)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
