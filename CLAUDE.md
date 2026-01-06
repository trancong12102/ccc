# Claude Skills Marketplace

A Claude Code plugin marketplace. See [README.md](README.md) for full documentation.

## Project Structure

```
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
name: Skill Name
description: Activate when [trigger conditions]. [What it does] for [use case].
version: 1.0.0
---

# Skill Name

Instructions...
```

## Skill Authoring Best Practices

### Activation & Triggers

- Skills are triggered by the `description` field in YAML frontmatter
- **DO NOT** add "When to Activate" sections - they are redundant
- Include trigger keywords in description: "Activate when creating X, doing Y, or running Z"
- Be specific: "Extract PDF text" > "Helps with documents"

### Description Format

```yaml
description: Activate when [trigger conditions]. [What it does] for [use case].
```

**Example:**

```yaml
description: Activate when creating git commits, committing changes, or writing commit messages. Generates semantic messages following Conventional Commits for changelog automation.
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
