---
name: Conventional Commit
description: Activate when creating git commits, committing changes, or writing commit messages. Generates semantic, machine-readable messages following the Conventional Commits specification for changelog automation and semantic versioning.
version: 1.1.0
---

# Conventional Commit

Generate commit messages following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## Commit Message Format

<format>

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]

```

</format>

## Commit Types Reference

<types>

| Type       | Description                                           | SemVer Impact |
| ---------- | ----------------------------------------------------- | ------------- |
| `feat`     | A new feature                                         | MINOR         |
| `fix`      | A bug fix                                             | PATCH         |
| `docs`     | Documentation only changes                            | -             |
| `style`    | Code style changes (formatting, whitespace)           | -             |
| `refactor` | Code change that neither fixes a bug nor adds feature | -             |
| `perf`     | Performance improvement                               | PATCH         |
| `test`     | Adding or modifying tests                             | -             |
| `build`    | Build system or external dependency changes           | -             |
| `ci`       | CI configuration changes                              | -             |
| `chore`    | Other changes that don't modify src or test files     | -             |
| `revert`   | Reverts a previous commit                             | -             |

</types>

## Workflow

Think step-by-step through this workflow before creating a commit.

### Step 1: Analyze Changes

Run these commands in parallel to understand the current state:

```bash
git status
git diff HEAD
git log --oneline -10
```

### Step 2: Evaluate and Classify

Before writing the commit message, analyze:

<analysis>

1. **What changed?** - List the files and modifications
2. **Why did it change?** - The motivation behind the change
3. **What type is this?** - Match against the types table above
4. **What scope?** - Which area of codebase (api, ui, auth, etc.)
5. **Is it breaking?** - Does it break backward compatibility?
6. **Are there related issues?** - Link with Fixes/Refs

</analysis>

### Step 3: Stage Changes

```bash
git add <files>
```

### Step 4: Create the Commit

Use a HEREDOC for proper multi-line formatting:

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

<body>

<footer>
EOF
)"
```

## Rules

<rules>

### Description Rules

- Use **imperative mood**: "add feature" not "added feature"
- Keep under 50 characters
- No period at end
- Be specific: "fix login timeout" not "fix bug"

### Scope Rules

- Use a noun describing the affected area
- Keep short (1-2 words)
- Be consistent across the project
- Examples: `api`, `ui`, `auth`, `parser`, `config`, `deps`

### Body Rules

- Separate from description with blank line
- Explain the **why**, not the what
- Wrap at 72 characters

### Breaking Change Rules

Indicate breaking changes using ONE of:

1. Exclamation mark: `feat(api)!: description`
2. Footer: `BREAKING CHANGE: description`

### Footer Tokens

- `BREAKING CHANGE:` - Breaking changes
- `Fixes #<issue>` - Closes an issue
- `Refs #<issue>` - References without closing
- `Co-authored-by:` - Multiple authors

</rules>

## Examples

<examples>

### Simple Feature

```text
feat(auth): add password reset functionality
```

### Bug Fix with Scope

```text
fix(api): handle null response from external service
```

### Feature with Body

```text
feat(dashboard): add real-time notifications

Implement WebSocket connection for push notifications.
Users can now receive instant updates without page refresh.
```

### Breaking Change

```text
feat(api)!: migrate to v2 authentication tokens

BREAKING CHANGE: JWT tokens now use RS256 algorithm instead of HS256.
All existing tokens will be invalidated. Users must re-authenticate.

Fixes #234
```

### Documentation Update

```text
docs(readme): update installation instructions for Node 20
```

### Multiple Footers

```text
fix(parser): resolve infinite loop on malformed input

The parser now validates input structure before processing,
preventing the recursive call that caused the infinite loop.

Fixes #123
Reviewed-by: Jane Doe <jane@example.com>
```

</examples>

## Anti-Patterns

<avoid>

| Bad | Why | Good |
|-----|-----|------|
| `fix bug` | Too generic | `fix(auth): resolve session timeout on idle` |
| `updated code` | No context | `refactor(api): extract validation logic` |
| `fixed` | Past tense | `fix` |
| `changes` | Meaningless | `feat(ui): add dark mode toggle` |
| `WIP` | Incomplete | Split into atomic commits |

</avoid>

## Safety Constraints

<constraints>

- Never use `-i` flag (interactive mode not supported)
- Never force push to main/master
- Never skip hooks unless explicitly requested
- Never commit secrets, credentials, or `.env` files
- Do not push unless explicitly asked
- Verify changes before committing

</constraints>

## Decision Tree

```text
Is it a new feature?
├── Yes → feat
└── No → Does it fix a bug?
    ├── Yes → fix
    └── No → Is it documentation only?
        ├── Yes → docs
        └── No → Is it a refactor (no behavior change)?
            ├── Yes → refactor
            └── No → Is it a performance improvement?
                ├── Yes → perf
                └── No → Is it test-related?
                    ├── Yes → test
                    └── No → Is it build/CI related?
                        ├── Yes → build or ci
                        └── No → chore
```
