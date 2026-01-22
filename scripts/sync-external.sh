#!/bin/bash
# Sync external skills from vendor submodules to external/skills

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Syncing external skills..."

# ast-grep skill
echo "  - ast-grep"
rm -rf "$ROOT_DIR/external/skills/ast-grep"
cp -r "$ROOT_DIR/vendor/ast-grep-agent-skill/ast-grep/skills/ast-grep" "$ROOT_DIR/external/skills/ast-grep"

echo "Done."
