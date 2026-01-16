#!/bin/bash
set -euo pipefail

input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // ""')

# Package manifest files
case "$file_path" in
  */package.json|*/requirements.txt|*/requirements-*.txt|*/pyproject.toml|*/Cargo.toml|*/go.mod|*/pom.xml|*/build.gradle|*/build.gradle.kts|*/*.csproj|*/packages.config)
    cat <<EOF
{
  "decision": "allow",
  "systemMessage": "REMINDER: When adding dependencies, consider using the latest-version skill to look up current versions. Run: python3 \$CLAUDE_PLUGIN_ROOT/skills/latest-version/scripts/get-versions.py <system> <packages>"
}
EOF
    ;;
  *)
    echo '{"decision": "allow"}'
    ;;
esac
