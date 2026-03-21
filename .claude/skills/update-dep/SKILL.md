---
name: update-dep
description: >-
  Use when the user asks to "update dependency", "bump dependency",
  "upgrade dep", "update unihan-etl", "bump unihan-etl", "update cihai dep",
  or wants to update a Python package dependency with atomic commits,
  upstream impact analysis, and PR creation. Handles both simple
  (no code changes) and complex (breaking API changes) updates.
user-invocable: true
argument-hint: "<package-name> [--to <version>] [--local-clone <path>]"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - WebFetch
  - AskUserQuestion
  - Agent
---

# Update Dependency

Update a Python package dependency with atomic commits following cihai project
conventions.

Parse `$ARGUMENTS` for the package name and optional flags. If `$ARGUMENTS` is
empty, ask the user which dependency to update.

| Flag | Effect |
|------|--------|
| `--to <version>` | Target version (default: latest tag in local clone or PyPI) |
| `--local-clone <path>` | Path to local clone of the upstream repo |

Read `references/cihai-projects.md` for known cihai ecosystem packages,
clone paths, docs URLs, and CHANGES anchor construction rules.

## Phase 1: Gather Context

### 1a. Current version

Read `pyproject.toml` and extract the current version constraint for the
target package. Note the constraint operator (`~=`, `>=`, `==`).

### 1b. Target version

If `--to` was provided, use that version. Otherwise:

**Local clone** (preferred): Check `references/cihai-projects.md` for known
clone paths. For cihai packages, try `~/work/cihai/<package-name>/`. Run:

```bash
git -C "$LOCAL_CLONE_PATH" fetch --tags && \
git -C "$LOCAL_CLONE_PATH" tag --sort=-version:refname | head -5
```

**PyPI fallback**: If no local clone exists:

```bash
pip index versions "$PACKAGE_NAME" 2>/dev/null | head -3
```

If target equals current, report "already up to date" and stop.

### 1c. Branch

Check the current branch name. The convention is `<package-name>-v<version>`.
If not already on the right branch, ask whether to create and switch.

## Phase 2: Research Upstream Changes

### 2a. Read upstream CHANGES

If a local clone exists, read the CHANGES file. Extract all version sections
between the current and target versions. Classify each section:
- **Breaking changes** = potential code impact
- **New features / CLI changes** = may need code updates
- **Documentation / CI / dev deps** = no downstream impact

### 2b. Upstream diff

```bash
git -C "$LOCAL_CLONE_PATH" log "v$CURRENT..v$TARGET" --oneline --no-merges
```

Focus on commits touching the public API surface (not docs/ci/test-only).

### 2c. Build See-also URLs

Construct the `See also:` URLs for commit messages. Read the exact CHANGES
heading for the target version and transform it into anchors.

Use the rules in `references/cihai-projects.md` for the two anchor formats:
- **GitHub**: dots stripped from version (`0410`)
- **Docs**: dots become hyphens (`0-41-0`)

For non-cihai packages, use only the GitHub CHANGES URL.

## Phase 3: Impact Analysis

### 3a. Find import sites

Search the current project for all imports from the target package:

```bash
grep -rn "from ${PACKAGE_MODULE} import\|import ${PACKAGE_MODULE}" src/ tests/
```

Replace hyphens with underscores for the module name.

### 3b. Cross-reference with upstream changes

For each import, check whether the imported symbol was modified upstream:
- Removed = **must fix**
- Renamed = **must fix**
- Signature changed = **must fix**
- Internal API (`_internal.`) moved = **check carefully**
- No change = **safe**

### 3c. Check test fixtures

If the upstream ships test data that this project's fixtures were copied from:

```bash
ls tests/fixtures/
```

Compare against the upstream fixture directory for changes.

### 3d. Classify complexity

| Classification | Criteria | Commits |
|---------------|----------|---------|
| **Simple** | No API changes affecting this project | 2 |
| **Moderate** | Minor API changes, symbol renames | 3-4 |
| **Complex** | Removed fields, new data formats, fixtures | 4+ |

### 3e. Confirm with user

Present:
1. Current → target version
2. Upstream change summary (breaking vs non-breaking)
3. Impact on this project (files needing changes)
4. Planned commit sequence
5. `See also:` URLs

Use `AskUserQuestion` with options: **Proceed**, **Research more**, **Cancel**.
Do not proceed without approval.

## Phase 4: Execute Update

### Quality gate

Run before each commit:

```bash
uv run ruff format . && \
uv run ruff check . --fix --show-fixes && \
uv run mypy src tests && \
uv run pytest
```

Fix any failures before committing. Never skip checks.

### Commit 1: Dependency version bump

Edit `pyproject.toml` to update the version constraint. Then:

```bash
uv lock
git add pyproject.toml uv.lock
```

Commit message:

```
py(deps) Bump <package> v<old> -> v<new>

See also:
- https://github.com/cihai/<package>/blob/v<new>/CHANGES#<github-anchor>
- https://<package>.git-pull.com/history.html#<docs-anchor>
```

Use heredoc for multi-line messages. Omit the docs URL for non-cihai packages.

### Commits 2+ (if needed): Code changes

Create one atomic commit per logical change. Common patterns:

**Removed field/symbol:**
```
constants: Remove <symbol>

See also:
- <upstream-reference>
```

**Updated type/enum:**
```
tables: Update <field> for <upstream-change>
```

**Import path change:**
```
<module>(fix): Update import from <old> to <new>
```

**Test fixture update:**
```
Data fixtures: Copy new test data from <package> <version>
```

For each: make the change, run the quality gate, stage only affected files,
commit.

### Final commit: CHANGES entry

Add an entry in the CHANGES file's current unreleased section. Insert after
the placeholder comments:

```
<!-- END PLACEHOLDER - ADD NEW CHANGELOG ENTRIES BELOW THIS LINE -->

<!-- Maintainers, insert changes / features for the next release here -->
```

**Simple update:**
```markdown

### Breaking changes

- Bump <package> v<old> -> v<new>
```

**Complex update:** Include subsections for updated/removed fields.

Stage and commit:

```bash
git add CHANGES
```

```
docs(CHANGES) Bump <package> v<old> -> v<new>

See also:
- https://github.com/cihai/<package>/blob/v<new>/CHANGES#<github-anchor>
- https://<package>.git-pull.com/history.html#<docs-anchor>
```

## Phase 5: Verify and PR

### 5a. Final check

Run the full quality gate one more time.

### 5b. Review commits

```bash
git log origin/master..HEAD --oneline
```

Verify: deps first, code changes middle, CHANGES last. Each commit has
proper `See also:` links.

### 5c. Push and create PR

```bash
git push -u origin "$(git branch --show-current)"
```

```bash
gh pr create --title "py(deps) Bump <package> v<old> -> v<new>" --body "$(cat <<'EOF'
## Summary

- Bump <package> from v<old> to v<new>
- <one-line upstream change summary>
- <impact: "No API changes" or "Updated X, removed Y">

## See also

- [<package> CHANGES](https://github.com/cihai/<package>/blob/v<new>/CHANGES)
- [<package> history](https://<package>.git-pull.com/history.html)

## Test plan

- [x] `uv run pytest` passes
- [x] `uv run mypy src tests` passes
- [x] `uv run ruff check .` passes
EOF
)"
```

### 5d. Update CHANGES with PR number

If the CHANGES entry lacks a PR number, update it now with the number from
`gh pr create` output and amend or create a fixup commit.

## Rules

- **Never** force-push or run destructive git commands
- **Never** push to `main` or `master` directly
- **Never** skip the quality gate
- **Always** present impact analysis before making changes
- **Always** use heredoc for multi-line commit messages
- **Always** include `See also:` links in dep bump and CHANGES commits
- **Deps first**: version bump commit always comes before code changes
- **CHANGES last**: changelog entry is always the final commit
- Stage specific files — never use `git add -A` or `git add .`
