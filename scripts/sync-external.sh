#!/bin/bash
# Sync external skills from vendor submodules to external/skills

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Syncing external skills..."

# logging-best-practices skill
echo "  - logging-best-practices"
rm -rf "$ROOT_DIR/external/skills/logging-best-practices"
cp -r "$ROOT_DIR/vendor/boristane-agent-skills/skills/logging-best-practices" "$ROOT_DIR/external/skills/logging-best-practices"

# react-best-practices skill
echo "  - react-best-practices"
rm -rf "$ROOT_DIR/external/skills/react-best-practices"
cp -r "$ROOT_DIR/vendor/vercel-agent-skills/skills/react-best-practices" "$ROOT_DIR/external/skills/react-best-practices"

# web-design-guidelines skill
echo "  - web-design-guidelines"
rm -rf "$ROOT_DIR/external/skills/web-design-guidelines"
cp -r "$ROOT_DIR/vendor/vercel-agent-skills/skills/web-design-guidelines" "$ROOT_DIR/external/skills/web-design-guidelines"

# design-postgres-tables skill
echo "  - design-postgres-tables"
rm -rf "$ROOT_DIR/external/skills/design-postgres-tables"
cp -r "$ROOT_DIR/vendor/timescale-pg-aiguide/skills/design-postgres-tables" "$ROOT_DIR/external/skills/design-postgres-tables"

echo "Done."
