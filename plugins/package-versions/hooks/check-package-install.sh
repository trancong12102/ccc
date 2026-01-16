#!/bin/bash
set -euo pipefail

input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // ""')

# Regex pattern for package install commands
# Uses \S (any non-whitespace) to match commands with flags before package names
# e.g., "npm install --save-dev jest" should trigger the reminder
pattern='(npm|yarn|pnpm|bun)\s+(add|install|i)\s+\S|(pip|pip3)\s+install\s+\S|cargo\s+add\s+\S|go\s+get\s+\S'

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
