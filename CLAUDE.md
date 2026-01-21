# Claude Skills Marketplace

A Claude Code plugin marketplace. See [README.md](README.md) for full documentation.

## Project Structure

```
ccc/
├── core/                    # Main plugin
│   ├── agents/              # Agent definitions (empty)
│   └── skills/              # Skill implementations
│       ├── brainstorming/
│       ├── context7/        # Library documentation lookup
│       │   └── references/
│       ├── conventional-commit/
│       ├── deps-dev/        # Package version lookup
│       ├── exa/             # Web search and crawling
│       │   └── references/
│       ├── oracle/          # Deep analysis via reasoning model
│       └── test-driven-development/
│           └── references/
├── .claude-plugin/
│   └── marketplace.json     # Marketplace registry
└── .markdownlint.json       # Markdown linting config
```

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
description: What the skill does. Use this skill when the user asks to [triggers]. Also use when [contextual trigger].
---

# Skill Name

Instructions...
```

## Skill Authoring Best Practices

### Activation & Triggers

- Skills are triggered by the `description` field in YAML frontmatter
- **The description IS the trigger mechanism** - there's no separate activation logic
- **DO NOT** add "When to Activate" sections in the body - they are redundant (body loads after triggering)
- Use semantic descriptions - Claude matches intent, not exact phrases
- Be specific about when to use: "commit changes" > "helps with git"

### Description Format

Follow this three-part structure:

```yaml
description: [What it does]. Use this skill when [triggers]. Also use [contextual trigger].
```

**Good example:**

```yaml
description: Generate semantic git commit messages following Conventional Commits. Use this skill when the user asks to commit, commit and push, save changes, or write a commit message. Also use after completing implementation tasks that need to be committed.
```

**Bad examples:**

```yaml
# Too vague - no specific triggers
description: Helps with git commits.

# Too verbose - unnecessary quoted phrases
description: This skill should be used when the user asks to "commit", "make a commit", "commit changes", or "/commit".

# Missing contextual trigger
description: Generate commit messages for git.
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
