# Claude Skills Marketplace

A Claude Code plugin marketplace. See [README.md](README.md) for full documentation.

## Project Structure

```bash
claude-skills/
├── .claude-plugin/
│   └── marketplace.json          # Plugin registry with full plugin definitions
├── plugins/
│   └── <plugin-name>/
│       ├── agents/*.md
│       ├── commands/*.md
│       └── skills/*/SKILL.md
└── docs/
```

## Adding a New Plugin

1. Create directory: `plugins/<plugin-name>/`
2. Add components:
   - `agents/*.md` - Agent definitions
   - `commands/*.md` - Slash commands
   - `skills/*/SKILL.md` - Skills
3. Register in `.claude-plugin/marketplace.json` with full plugin definition

## Marketplace Entry Format

```json
{
  "name": "marketplace-name",
  "description": "Marketplace description",
  "owner": { "name": "Owner", "email": "email@example.com" },
  "plugins": [
    {
      "name": "plugin-name",
      "version": "1.0.0",
      "description": "What the plugin does (min 10 chars)",
      "source": "./plugins/plugin-name",
      "category": "development",
      "tags": ["tag1", "tag2"],
      "skills": ["./skills/my-skill"],
      "license": "MIT"
    }
  ]
}
```

## Categories

Available: `development`, `productivity`, `utilities`, `documentation`, `testing`, `security`, `devops`, `data`

## Versioning

Plugin versions follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Naming Conventions

- Use **kebab-case** for all names
- Plugin names: `my-plugin`
- Commands: `my-command.md`
- Agents: `my-agent.md`
- Skills: `./skills/my-skill` (directory path, not SKILL.md)

## Component Formats

### Command (commands/*.md)

```markdown
---
name: command-name
description: What the command does
---

# Command Name

Instructions...
```

### Agent (agents/*.md)

```markdown
---
description: Agent role and expertise
capabilities:
  - Capability 1
  - Capability 2
---

# Agent Name

Instructions...
```

### Skill (skills/*/SKILL.md)

```markdown
---
name: skill-name
description: This skill should be used when the user asks to "trigger phrase 1", "trigger phrase 2", or "trigger phrase 3". Also use when [additional context]. [What it does].
---

# Skill Name

Instructions...
```

## Skill Authoring Best Practices

### Activation & Triggers

- Skills are triggered by the `description` field in YAML frontmatter
- **The description IS the trigger mechanism** - there's no separate activation logic
- **DO NOT** add "When to Activate" sections in the body - they are redundant (body loads after triggering)
- Use **third-person format**: "This skill should be used when..."
- Include **quoted trigger phrases** with exact words users would say
- Be specific: "commit changes" > "helps with git"

### Description Format

Use third-person format with specific trigger phrases:

```yaml
description: This skill should be used when the user asks to "phrase 1", "phrase 2", or "phrase 3". Also use when [context]. [What it does].
```

**Good example:**

```yaml
description: This skill should be used when the user asks to "commit", "make a commit", "commit changes", "write a commit message", "run git commit", or "/commit". Also use when Claude needs to commit after implementing changes or completing a task. Generates semantic, machine-readable git commit messages following the Conventional Commits specification.
```

**Bad examples:**

```yaml
# Too vague - no specific triggers
description: Helps with git commits.

# Missing quoted phrases
description: Use this skill when working with commits or git.

# First-person format
description: Use this skill when you need to commit code.
```

### Content Structure

```markdown
# Skill Name

Brief intro paragraph.

## [Reference Section]
Tables, formats, types for quick lookup.

## Workflow
Step-by-step instructions with "Think step-by-step" trigger.

## Rules
Grouped constraints and guidelines.

## Examples
Concrete examples wrapped for clarity.

## Anti-Patterns
Bad/Why/Good comparison table.

## Safety Constraints
Hard rules and limitations.
```

### Claude 4.5 Prompting Best Practices

Apply these when writing skill instructions:

1. **Use XML tags** for structured sections (optional, triggers lint warnings)
   - Add blank lines before and after XML tags for proper markdown rendering:

   ```markdown
   ## Section

   <tagname>

   Content here...

   </tagname>

   ## Next Section
   ```

2. **"Think step-by-step"** - Add this phrase before complex workflows
3. **Provide examples** - Show concrete good/bad patterns
4. **Be explicit** - Detailed instructions, no ambiguity
5. **Decision trees** - Visual flowcharts for classification tasks
6. **Anti-patterns table** - Bad | Why | Good format

### Size Guidelines

- Keep under **500 lines**
- Use progressive disclosure for details >100 lines
- Assume Claude knows basics - only include necessary guidance

### Avoiding Shell Parse Errors

Backticks in skill markdown can be misinterpreted as shell command substitution. Avoid patterns where text between backticks looks like a command:

**Problematic:**

```markdown
- Use `!` marker OR `BREAKING CHANGE:` footer
```

The pattern `` `!` marker OR ` `` gets parsed as a shell command, causing "command not found" errors.

**Safe alternatives:**

```markdown
- Add exclamation mark after type/scope or add BREAKING CHANGE: footer
- Use the exclamation mark (!) or BREAKING CHANGE: footer
```
