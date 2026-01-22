# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Claude Skills Marketplace** - a curated collection of Claude Code plugins with skills, commands, agents, and MCP server configurations. Skills are documentation-driven, defined in Markdown files with YAML frontmatter rather than traditional source code.

## Commands

```bash
# Sync external skills from vendor submodules
bash scripts/sync-external.sh

# Test plugin installation locally
/plugin install .
```

## Architecture

### Directory Structure

- `core/skills/` - Native marketplace skills (add new skills here)
- `external/skills/` - Synced from vendor submodules (do not edit directly)
- `vendor/` - Git submodules pointing to third-party repositories
- `scripts/` - Maintenance and sync scripts

### Skill Definition Format

Each skill is a `SKILL.md` file with:
1. **YAML frontmatter** - Required fields: `name`, `description`
2. **Markdown content** - Instructions that guide Claude on how to perform the skill

Example structure:
```markdown
---
name: skill-name
description: "When to use this skill and what it does"
---

# Skill Title

## Overview
What the skill does...

## Tool Usage
How to use Claude Code tools...

## The Process
Step-by-step guidance...
```

### Vendoring Pattern

External skills are managed via git submodules in `/vendor`. The sync script (`scripts/sync-external.sh`) copies specific skills to `/external/skills/`. To add a new external skill:
1. Add/update the submodule in `/vendor`
2. Add a copy command in `sync-external.sh`
3. Run `bash scripts/sync-external.sh`

## Skill Development Guidelines

- Place new skills in `core/skills/<skill-name>/SKILL.md`
- The `description` field determines when the skill is invoked - make it specific with trigger phrases
- Use structured tools like `AskUserQuestion` for user interaction
- Never modify files in `external/skills/` directly - they are overwritten by the sync script
