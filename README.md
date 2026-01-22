# Claude Skills Marketplace

> A curated marketplace of Claude Code plugins with skills, commands, agents, and MCP server configurations.

## Quick Start

### Step 1: Add the Marketplace

```bash
/plugin marketplace add trancong12102/ccc
```

### Step 2: Install Plugins

```bash
# Browse available plugins
/plugin

# Install core plugin
/plugin install ccc-core@ccc

# Install external skills plugin
/plugin install ccc-external@ccc
```

## Use with Other Coding Agents

Install skills using Vercel's add-skill:

```bash
bunx add-skill -a antigravity -y -g trancong12102/ccc
```

## Available Skills

| Skill | Description |
|-------|-------------|
| **brainstorming** | Collaboratively explore ideas through guided dialogue before implementation |
| **context7** | Look up documentation for any library using Context7 |
| **commit** | Generate git commit messages following Conventional Commits spec |
| **deps-dev** | Look up latest package versions using deps.dev API |
| **exa** | Web search, crawling, and code context retrieval |
| **oracle** | Deep analysis via powerful reasoning model (Codex CLI) |
| **test-driven-development** | Guide strict TDD using Red-Green-Refactor cycle |

## External Skills (ccc-external)

Skills synced from third-party repositories. These are automatically checked for updates daily.

| Skill | Source | Description |
|-------|--------|-------------|
| **logging-best-practices** | [boristane/agent-skills](https://github.com/boristane/agent-skills) | Logging best practices focused on wide events for debugging and analytics |
| **react-best-practices** | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | React and Next.js performance optimization guidelines |
| **web-design-guidelines** | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Web interface design guidelines for UI code review |

## Recommended Marketplaces

These community skills work great alongside this marketplace:

| Repository | Description |
|------------|-------------|
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Browser automation for web testing, form filling, screenshots, and data extraction |
| [ast-grep/claude-skill](https://github.com/ast-grep/claude-skill) | Structural code search using AST patterns |

Install external skills:

```bash
# Using Claude Code
/plugin marketplace add <owner>/<repo>

# Using add-skill (for other agents)
bunx add-skill -a antigravity -y -g <owner>/<repo>
```

## Prerequisites

Some skills require API keys to be set as environment variables:

| Variable | Skill | Description |
|----------|-------|-------------|
| `CONTEXT7_API_KEY` | context7 | API key for Context7 documentation lookup |
| `EXA_API_KEY` | exa | API key for Exa web search and content extraction |

## Setup Notes

### Enable Marketplace Auto-Update

To keep your plugins up to date automatically, enable marketplace auto-update in your Claude Code settings:

```bash
claude config set plugins.marketplace.auto_update true
```

### Oracle Skill

The oracle skill requires **Codex CLI** to be installed. Install it and configure the profile below to enable invoking gpt-5.2 (xhigh) for complex reasoning tasks.

Add this profile to your Codex `config.toml`:

```toml
[profiles.oracle]
model = "gpt-5.2"
model_reasoning_effort = "xhigh"
approval_policy = "never"
sandbox_mode = "read-only"

[sandbox_workspace_write]
network_access = true

[features]
web_search_request = true
```

See the [Codex CLI documentation](https://github.com/openai/codex) for setup instructions.

## License

MIT License
