# CLAUDE.md — AI Assistant Guide for NKN

## Repository Overview

**NKN** is a freshly initialized repository owned by Nknobody. At the time of this writing, the repository contains only a LICENSE file (The Unlicense / public domain). No source code, dependencies, or configuration files have been added yet.

This file serves as the canonical reference for AI assistants (Claude Code and similar tools) working in this repository.

---

## Current Repository State

```
NKN/
├── .git/
├── CLAUDE.md        # This file
└── LICENSE          # The Unlicense (public domain)
```

- **License**: The Unlicense — software is dedicated to the public domain. Anyone may use, modify, and distribute it without restriction.
- **Default branch**: `master`
- **Remote**: `origin` → `http://local_proxy@127.0.0.1:38645/git/Nknobody/NKN`

---

## Git Workflow

### Branch Naming

Claude Code development branches follow this pattern:
```
claude/<task-slug>-<session-id>
```
Example: `claude/claude-md-mmjjsots9aixuymr-H9vC3`

Always develop on the designated branch. Never push to `master` without explicit permission.

### Standard Git Operations

```bash
# Create and switch to a feature branch
git checkout -b claude/<task-name>-<session-id>

# Stage and commit changes
git add <specific-files>
git commit -m "Short imperative summary of change"

# Push to remote
git push -u origin <branch-name>
```

**Push retry policy**: If a push fails due to network errors, retry up to 4 times with exponential backoff (2s, 4s, 8s, 16s). Do not retry on HTTP 403 errors — that indicates a branch naming or permissions issue.

### Commit Message Conventions

- Use the imperative mood: "Add feature", not "Added feature"
- Keep the subject line under 72 characters
- Separate subject from body with a blank line (if body is needed)
- Reference issue numbers when applicable: `Fix #42: ...`

---

## Development Guidelines for AI Assistants

Since this project has no code yet, these are the conventions to follow when adding content:

### General Principles

- **Minimal by default**: Only add what is directly requested. Avoid scaffolding files "just in case".
- **No speculative abstractions**: Don't create helpers, utilities, or wrappers for hypothetical future use.
- **No unsolicited documentation**: Don't add docstrings, comments, or type annotations to code you didn't write or change.
- **No backwards-compat shims**: Don't add compatibility layers unless explicitly asked.
- **Security first**: Avoid introducing OWASP Top 10 vulnerabilities (injection, XSS, broken auth, etc.).

### When Adding a New Language/Stack

Before writing any code, confirm with the user:
1. Language and version (e.g., Python 3.12, Go 1.22, Node.js 22)
2. Framework (if any)
3. Dependency manager (pip/uv, go mod, npm/pnpm, cargo, etc.)
4. Testing framework preferences

Then create the minimal necessary files:
- A dependency/module file (`package.json`, `go.mod`, `requirements.txt`, etc.)
- A `.gitignore` appropriate for the language
- Source entry point
- A basic test file

### Adding CI/CD

Place GitHub Actions workflows under `.github/workflows/`. Use concise, descriptive workflow file names (e.g., `ci.yml`, `release.yml`).

---

## File & Directory Conventions (To Be Established)

These will be defined as the project grows. Update this file when conventions are established:

| Convention | Value |
|---|---|
| Source directory | TBD |
| Test directory | TBD |
| Build output | TBD |
| Environment config | TBD |
| Code style / linter | TBD |

---

## Updating This File

This CLAUDE.md should be kept up to date. Update it whenever:
- A language, framework, or major dependency is added
- Build, test, or lint commands are established
- New architectural decisions are made
- Directory structure changes significantly

---

*Last updated: 2026-03-09*
