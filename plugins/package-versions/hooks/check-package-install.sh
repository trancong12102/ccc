#!/bin/bash
set -euo pipefail

input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // ""')

# Regex pattern for package install commands
pattern='(npm|yarn|pnpm|bun)\s+(add|install|i)\s+[^-]|(pip|pip3)\s+install\s+[^-]|cargo\s+add\s+|go\s+get\s+'

if echo "$command" | grep -qE "$pattern"; then
  cat <<EOF
{
  "decision": "allow",
  "systemMessage": "REMINDER: Before installing packages, consider using the latest-version skill to look up current versions. Run: python3 \$CLAUDE_PLUGIN_ROOT/skills/latest-version/scripts/get-versions.py <system> <packages>"
}
EOF
else
  echo '{"decision": "allow"}'
fi
