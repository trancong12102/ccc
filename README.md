# Claude Skills Marketplace

> A curated marketplace of Claude Code plugins with skills, commands, agents, and MCP server configurations.

## Quick Start

### Step 1: Add the Marketplace

```bash
/plugin marketplace add trancong12102/claude-skills
```

### Step 2: Install Plugins

```bash
# Browse available plugins
/plugin

# Install a plugin
/plugin install <plugin-name>@claude-skills
```

Each plugin loads **only its specific agents, commands, and skills** into Claude's context.

## Available Plugins

See [Plugin Reference](docs/plugins.md) for the complete catalog.

## Documentation

- **[Plugin Reference](docs/plugins.md)** - Complete catalog of all plugins
- **[Usage Guide](docs/usage.md)** - Commands, workflows, and best practices

## Contributing

To add a new plugin:

1. Create a directory in `plugins/` with the plugin name
2. Add `.claude-plugin/plugin.json` manifest
3. Add components in `agents/`, `commands/`, `skills/`
4. Register the plugin in `.claude-plugin/marketplace.json`

### Plugin Structure

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json         # Required manifest
├── agents/                 # Agent definitions (.md)
├── commands/               # Slash commands (.md)
├── skills/                 # Skills (subdirectories with SKILL.md)
│   └── my-skill/
│       └── SKILL.md
└── .mcp.json              # Optional MCP servers
```

## License

MIT License
