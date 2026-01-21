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
```

## Available Skills

| Skill | Description |
|-------|-------------|
| **brainstorming** | Collaboratively explore ideas through guided dialogue before implementation |
| **context7** | Look up documentation for any library using Context7 |
| **conventional-commit** | Generate git commit messages following Conventional Commits spec |
| **deps-dev** | Look up latest package versions using deps.dev API |
| **exa** | Web search, crawling, and code context retrieval |
| **oracle** | Deep analysis via powerful reasoning model (Codex MCP) |
| **test-driven-development** | Guide strict TDD using Red-Green-Refactor cycle |

## Setup Notes

### Oracle Skill

The oracle skill requires **Codex MCP** to be configured in Claude Code (or other agents). Add the Codex MCP server to your configuration to enable invoking gpt-5.2 (xhigh) for complex reasoning tasks.

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

See the [Codex MCP documentation](https://github.com/openai/codex) for setup instructions.

## License

MIT License
