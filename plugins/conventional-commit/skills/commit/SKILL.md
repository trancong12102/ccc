---
name: conventional-commit
description: Generate semantic, machine-readable git commit messages. Use this skill when the user asks to commit, make a commit, commit changes, write a commit message, or run git commit. Follows the Conventional Commits specification for changelog automation and semantic versioning.
---

# Conventional Commit

Generate commit messages following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## Commit Message Format

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Decision Tree: Choosing Commit Type

```text
What kind of change is this?
├─ New feature → feat
├─ Bug fix → fix
├─ Documentation only → docs
├─ Code style (formatting, whitespace) → style
├─ Refactor (no behavior change) → refactor
├─ Performance improvement → perf
├─ Tests → test
├─ Build system/dependencies → build
├─ CI configuration → ci
├─ Reverts previous commit → revert
└─ Other (doesn't modify src/test) → chore
```

## Commit Types Reference

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

## Workflow

**Before committing**, run these commands in parallel to understand the current state:

```bash
git status
git diff HEAD
git log --oneline -10
```

**Then analyze**:
1. What changed and why?
2. Which type best describes this change?
3. What scope applies (api, ui, auth, etc.)?
4. Is this a breaking change?
5. Are there related issues to link?

**Stage and commit**:

```bash
git add <files>
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

<body>

<footer>
EOF
)"
```

## Best Practices

- **Use imperative mood**: "add feature" not "added feature"
- **Keep description under 50 characters**, no period at end
- **Body explains the why**, not the what - wrap at 72 characters
- **Scope is a noun** describing affected area: `api`, `ui`, `auth`, `parser`
- **Breaking changes**: Add `!` after type/scope or use `BREAKING CHANGE:` in footer

## Footer Tokens

- `BREAKING CHANGE:` - Breaking API changes
- `Fixes #<issue>` - Closes an issue
- `Refs #<issue>` - References without closing
- `Co-authored-by:` - Multiple authors

## Examples

**Simple feature:**
```text
feat(auth): add password reset functionality
```

**Bug fix with scope:**
```text
fix(api): handle null response from external service
```

**Feature with body:**
```text
feat(dashboard): add real-time notifications

Implement WebSocket connection for push notifications.
Users can now receive instant updates without page refresh.
```

**Breaking change:**
```text
feat(api)!: migrate to v2 authentication tokens

BREAKING CHANGE: JWT tokens now use RS256 algorithm instead of HS256.
All existing tokens will be invalidated. Users must re-authenticate.

Fixes #234
```

## Common Pitfalls

❌ **Don't** use generic messages like `fix bug` or `updated code`
✅ **Do** be specific: `fix(auth): resolve session timeout on idle`

❌ **Don't** use past tense: `fixed`, `added`, `changed`
✅ **Do** use imperative: `fix`, `add`, `change`

❌ **Don't** commit incomplete work as `WIP`
✅ **Do** split into atomic, complete commits

## Safety Constraints

- Never use `-i` flag (interactive mode not supported)
- Never force push to main/master
- Never skip hooks unless explicitly requested
- Never commit secrets, credentials, or `.env` files
- Do not push unless explicitly asked
