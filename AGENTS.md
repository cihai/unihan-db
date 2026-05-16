# AGENTS.md

Guidance for AI agents (e.g., Claude Code, Cursor, GPT-based tools) working in this repository.

## CRITICAL REQUIREMENTS

### Test Success
- ALL tests MUST pass for work to be complete
- Never claim code "works" if any test fails
- Failing tests anywhere mean the codebase is broken and must be fixed
- Changes that break existing tests are not done until fixed
- A finished change passes linting, type checking, and the full test suite

## Project Overview

gp-libs (this repo packages the `unihan_db` library) provides SQLAlchemy models and helpers to load the Unicode UNIHAN dataset. It is part of the cihai/gp-libs family and is powered by [`unihan-etl`](https://unihan-etl.git-pull.com).

Key features:
- Bootstrap UNIHAN data from official sources (via `unihan-etl`) into SQLAlchemy models
- Default SQLite database stored in the user's XDG data dir (see `unihan_db.dirs`)
- Helper utilities to convert ORM rows to dictionaries (`bootstrap.to_dict`)
- Ships fixtures and example script (`examples/01_bootstrap.py`) to seed and query data

## Development Environment

This project uses:
- Python 3.10+ (<4.0)
- [uv](https://github.com/astral-sh/uv) for dependency management (see `uv.lock` / dependency-groups)
- [ruff](https://github.com/astral-sh/ruff) for linting/formatting
- [mypy](https://github.com/python/mypy) for type checking
- [pytest](https://docs.pytest.org/) for tests (with doctest support in fixtures)
- [Sphinx](https://www.sphinx-doc.org/) for documentation

## Common Commands

### Setting Up Environment

```bash
# Install runtime deps
uv pip install --editable .

# Install with dev tools (ruff, mypy, pytest, docs, etc.)
uv pip install --editable . -G dev

# Sync exactly to lockfile
uv pip sync
```

### Running Tests

```bash
# Run full suite
just test        # wraps uv run py.test
uv run pytest    # equivalent

# Single file / test
uv run pytest tests/test_bootstrap.py
uv run pytest tests/test_bootstrap.py::test_import_unihan_raw

# Continuous testing
just start       # just test then uv run ptw .
uv run ptw .     # pytest-watcher
```

### Linting and Type Checking

```bash
# Ruff lint
just ruff
uv run ruff check . --fix --show-fixes

# Format with ruff
just ruff-format
uv run ruff format .

# mypy
just mypy
uv run mypy src tests

# Watchers (requires entr)
just watch-ruff
just watch-mypy
```

### Documentation

```bash
just build-docs   # sphinx html
just start-docs   # sphinx autobuild server
just design-docs  # rebuild CSS/JS assets
```

## Development Workflow

1) Format: `uv run ruff format .`
2) Run tests: `uv run pytest`
3) Lint: `uv run ruff check . --fix --show-fixes`
4) Type-check: `uv run mypy`
5) Re-run tests to confirm green

## Code Architecture

1. **`src/unihan_db/bootstrap.py`** – logging setup, default UNIHAN file/field lists, ETL options merge, data download via `unihan-etl`, `bootstrap_unihan` to populate the database, `to_dict` helpers, and `get_session` to create a scoped SQLAlchemy session (defaults to SQLite in XDG data dir).
2. **`src/unihan_db/importer.py`** – transforms normalized UNIHAN records into ORM objects, wiring relations for readings, locations, variants, and indexes before commit.
3. **`src/unihan_db/tables.py`** – SQLAlchemy ORM models (`Base`, `Unhn`, and many related tables for readings, strokes, variants, etc.).
4. **`src/unihan_db/__init__.py`** – establishes XDG directories via `appdirs`/`unihan_etl.AppDirs`, creating the data dir on import.
5. **`src/unihan_db/__about__.py`** – package metadata (version).
6. **Examples** – `examples/01_bootstrap.py` demonstrates bootstrapping and querying random rows.

## Data Flow & Defaults

- `bootstrap.bootstrap_data` calls `unihan_etl.core.Packager` with default UNIHAN file list (`UNIHAN_FILES`) and field list (`UNIHAN_FIELDS`).
- `bootstrap.bootstrap_unihan` inserts rows only when `Unhn` is empty, batching for speed and committing once.
- Default database URL template is `sqlite:///{user_data_dir}/unihan_db.db`; `dirs.user_data_dir` comes from XDG on the current OS.

## Testing Strategy

- Pytest fixtures live in `tests/conftest.py` and `conftest.py` (root) to support doctests.
- Fixtures provide in-memory SQLite engine, scoped sessions, and a zipped UNIHAN fixture built from `tests/fixtures/` using `UNIHAN_FILES` list.
- Tests avoid network by zipping local fixture files; rely on `unihan_options` fixture for ETL options.
- Example script is executed in tests (`tests/test_example.py`) to ensure docs stay runnable.

### Testing Guidelines
- Prefer provided fixtures (`engine`, `session`, `unihan_options`, `zip_file`, `project_root`) over ad-hoc setup.
- Keep tests deterministic—no external downloads; use fixtures in `tests/fixtures`.
- Use `tmp_path`/`tmpdir` fixtures for filesystem writes; root conftest auto-sets `HOME` and cwd to temp paths.
- If adding doctests, ensure fixtures are wired via `add_doctest_fixtures` in root conftest.

### Example Fixture Usage

```python
def test_can_round_trip_char(session, engine):
    from unihan_db.tables import Base, Unhn

    Base.metadata.create_all(engine)
    session.add(Unhn(char="好", ucn="U+597D"))
    session.commit()

    assert session.query(Unhn).count() == 1
```

## Coding Standards

- Include `from __future__ import annotations` in Python modules.
- Prefer namespace imports for stdlib (`import typing as t`) to keep type usage explicit; third-party packages may use `from X import Y`.
- Use Ruff for style/formatting; keep docstrings in NumPy/reST sections (`Parameters`, `Returns`).
- Align with existing patterns: SQLAlchemy ORM models, scoped sessions, and helper functions in `bootstrap.py`.

## Logging Standards

These rules guide future logging changes; existing code may not yet conform.

### Logger setup

- Use `logging.getLogger(__name__)` in every module
- Add `NullHandler` in library `__init__.py` files
- Never configure handlers, levels, or formatters in library code — that's the application's job

### Structured context via `extra`

Pass structured data on every log call where useful for filtering, searching, or test assertions.

**Core keys** (stable, scalar, safe at any log level):

| Key | Type | Context |
|-----|------|---------|
| `unihan_field` | `str` | UNIHAN field name |
| `unihan_source_file` | `str` | source data file path |
| `unihan_record_count` | `int` | records processed |
| `unihan_db_table` | `str` | database table name |
| `unihan_db_rows` | `int` | rows affected |

**Heavy/optional keys** (DEBUG only, potentially large):

| Key | Type | Context |
|-----|------|---------|
| `unihan_stdout` | `list[str]` | subprocess stdout lines (truncate or cap; `%(unihan_stdout)s` produces repr) |
| `unihan_stderr` | `list[str]` | subprocess stderr lines (same caveats) |

Treat established keys as compatibility-sensitive — downstream users may build dashboards and alerts on them. Change deliberately.

### Key naming rules

- `snake_case`, not dotted; `unihan_` prefix
- Prefer stable scalars; avoid ad-hoc objects
- Heavy keys (`unihan_stdout`, `unihan_stderr`) are DEBUG-only; consider companion `unihan_stdout_len` fields or hard truncation (e.g. `stdout[:100]`)

### Lazy formatting

`logger.debug("msg %s", val)` not f-strings. Two rationales:
- Deferred string interpolation: skipped entirely when level is filtered
- Aggregator message template grouping: `"Running %s"` is one signature grouped ×10,000; f-strings make each line unique

When computing `val` itself is expensive, guard with `if logger.isEnabledFor(logging.DEBUG)`.

### stacklevel for wrappers

Increment for each wrapper layer so `%(filename)s:%(lineno)d` and OTel `code.filepath` point to the real caller. Verify whenever call depth changes.

### LoggerAdapter for persistent context

For objects with stable identity (Dataset, Reader, Exporter), use `LoggerAdapter` to avoid repeating the same `extra` on every call. Lead with the portable pattern (override `process()` to merge); `merge_extra=True` simplifies this on Python 3.13+.

### Log levels

| Level | Use for | Examples |
|-------|---------|----------|
| `DEBUG` | Internal mechanics, data I/O | Field parsing, record transformation steps |
| `INFO` | Data lifecycle, user-visible operations | Download completed, export finished, database bootstrapped |
| `WARNING` | Recoverable issues, deprecation, user-actionable config | Missing optional field, deprecated data format |
| `ERROR` | Failures that stop an operation | Download failed, parse error, database write failed |

Config discovery noise belongs in `DEBUG`; only surprising/user-actionable config issues → `WARNING`.

### Message style

- Lowercase, past tense for events: `"download completed"`, `"parse error"`
- No trailing punctuation
- Keep messages short; put details in `extra`, not the message string

### Exception logging

- Use `logger.exception()` only inside `except` blocks when you are **not** re-raising
- Use `logger.error(..., exc_info=True)` when you need the traceback outside an `except` block
- Avoid `logger.exception()` followed by `raise` — this duplicates the traceback. Either add context via `extra` that would otherwise be lost, or let the exception propagate

### Testing logs

Assert on `caplog.records` attributes, not string matching on `caplog.text`:
- Scope capture: `caplog.at_level(logging.DEBUG, logger="unihan_db.bootstrap")`
- Filter records rather than index by position: `[r for r in caplog.records if hasattr(r, "unihan_field")]`
- Assert on schema: `record.unihan_record_count == 100` not `"100 records" in caplog.text`
- `caplog.record_tuples` cannot access extra fields — always use `caplog.records`

### Avoid

- f-strings/`.format()` in log calls
- Unguarded logging in hot loops (guard with `isEnabledFor()`)
- Catch-log-reraise without adding new context
- `print()` for diagnostics
- Logging secret env var values (log key names only)
- Non-scalar ad-hoc objects in `extra`
- Requiring custom `extra` fields in format strings without safe defaults (missing keys raise `KeyError`)

## Git Commit Standards

Commit subjects: `Scope(type[detail]): concise description`

Body template:
```
why: Reason or impact.
what:
- Key technical changes
- Single topic only
```

Guidelines:
- Subject ≤50 chars; body lines ≤72 chars; imperative mood.
- One topic per commit; separate subject and body with a blank line.

Common commit types:
- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (CLAUDE.md)
- **ai(claude[command])**: Claude Code command changes

## Documentation Standards

### Code Blocks in Documentation

When writing documentation (README, CHANGES, docs/), follow these rules for code blocks:

**One command per code block.** This makes commands individually copyable.

**Put explanations outside the code block**, not as comments inside.

Good:

Run the tests:

```console
$ uv run pytest
```

Run with coverage:

```console
$ uv run pytest --cov
```

Bad:

```console
# Run the tests
$ uv run pytest

# Run with coverage
$ uv run pytest --cov
```

### Changelog Conventions

These rules apply when authoring entries in `CHANGES`, which is rendered as the Sphinx changelog page. Modeled on Django's release-notes shape — deliverables get titles and prose, not bullets. Older entries used a flat `### Section` + bullet shape; new entries follow the Django shape below.

**Release entry boilerplate.** Every release header is `## unihan-db X.Y.Z (YYYY-MM-DD)`. The file opens with a `## unihan-db X.Y.Z (unreleased)` placeholder block fenced by `<!-- KEEP THIS PLACEHOLDER ... -->` and `<!-- END PLACEHOLDER ... -->` HTML comments — new release entries land immediately below the END marker, never above it.

**Open with a multi-sentence lead paragraph.** Plain prose, no italic. Open with the version as sentence subject (*"unihan-db X.Y.Z ships …"*) so the lead is self-contained when excerpted. Two to four sentences telling the reader what shipped and who cares — user-visible takeaways, not internal mechanism. Cross-reference detail docs with `{ref}` to keep the lead compact.

**Each deliverable is a section, not a bullet.** Inside `### What's new`, every distinct deliverable gets a `#### Deliverable title (#NN)` heading naming it in user vocabulary, followed by 1-3 prose paragraphs explaining what shipped. Don't wrap a paragraph in `- ` — bullets are for enumerable lists, not paragraph containers. Cross-link detail docs (`See {ref}\`foo\` for details.`) so prose stays focused.

**The deliverable test.** Before writing an entry, ask: "What's the deliverable, in user vocabulary?" If you can't answer in one sentence, the entry isn't ready. Mechanism (helper internals, byte counters, schema-validation locations) belongs in PR descriptions and code comments, not the changelog.

**Fixed subheadings**, in this order when present: `### Breaking changes`, `### Dependencies`, `### What's new`, `### Fixes`, `### Documentation`, `### Development`. Dev tooling (helper scripts, internal automation) lives under `### Development`. For breaking changes, show the migration path with concrete inline code (e.g. a `# Before` / `# After` fenced code block). Dependency floor bumps use the form ``Minimum `pkg>=X.Y.Z` (was `>=X.Y.W`)``.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**When bullets are appropriate.** Catch-all sections (`### Fixes`, occasionally `### Documentation`) with 3+ genuinely small items use bullets — one line each, never paragraphs. If a bullet swells past two lines, promote it to a `#### Title (#NN)` heading with prose body.

**Anti-patterns.**

- Fragile metrics: token ceilings, third-party version pins, percent benchmarks, exact byte counts. Describe the *capability*, not the math.
- Internal jargon: private symbols (leading-underscore identifiers), algorithm names exposed for the first time, backend scaffolding.
- Walls of text dressed up as bullets.
- Buried breaking changes — they get their own subheading at the top of the entry.

**Always link autodoc'd APIs.** Any class, method, function, exception, or attribute that has its own rendered page must be cited via the appropriate role (`{class}`, `{meth}`, `{func}`, `{exc}`, `{attr}`) — never with plain backticks. Doc pages without explicit ref labels use `{doc}`. Plain backticks are correct for code syntax, env vars, parameter names, and file paths that aren't doc pages — anything without an autodoc destination.

**MyST roles.** Class references use `{class}`, methods use `{meth}`, functions use `{func}`, exceptions use `{exc}`, attributes use `{attr}`, internal anchors use `{ref}`, doc-path links use `{doc}`.

**Summarization style.** When a user asks "what changed in the latest version?" or similar, lead with the entry's lead paragraph (paraphrased if needed), followed by each `####` deliverable heading under `### What's new` with a one-sentence summary. Cite `(#NN)` only if the user asks for source links. Don't invent versions, dates, or numbers not present in `CHANGES`. Don't quote line numbers or file offsets — those shift as the file evolves.

## Debugging Tips

- When ETL runs slowly, log level INFO in `bootstrap` already streams progress; avoid adding noisy prints.
- If objects look stale, recreate sessions or re-run `Base.metadata.create_all` against your engine in tests.
- Use the provided fixtures to keep paths isolated—tests assume `HOME` and cwd are temporary.

## gp-libs/cihai References

- Docs: https://unihan-db.git-pull.com/
- API: https://unihan-db.git-pull.com/api.html
- Dataset: https://www.unicode.org/charts/unihan.html
- unihan-etl: https://unihan-etl.git-pull.com

## Shipped vs. Branch-Internal Narrative

Long-running branches accumulate tactical decisions — renames,
refactors, attempts-then-reverts, intermediate states. Commit messages
and the diff hold *what changed* and *why*. Do not restate either in
artifacts the downstream reader holds: code, docstrings, README,
CHANGES, PR descriptions, release notes, migration guides.

When deciding what counts as branch-internal, use trunk or the parent
branch as the baseline — not intermediate states inside the current
branch.

**The Published-Release Test**

Before adding rename history, "previously" / "formerly" / "no longer
X" phrasing, "removed" / "moved" / "refactored" / "fixed" diff
paraphrases, or `### Fixes` entries to a user-facing surface, ask:

> Did users of the most recently published release ever experience
> this old name, old behavior, or bug?

If the answer is no, it is branch-internal narrative. Move it to the
commit message and describe only the current state in the artifact.

**Keep in shipped artifacts**

- Deprecations and migration guides for symbols that actually shipped.
- `### Fixes` entries for bugs that affected users of a published
  release.
- Comments explaining *why the current code looks this way* —
  invariants, platform quirks, upstream bug workarounds — that make
  sense to a reader who never saw the previous version.

**Default**: when in doubt, keep the artifact clean and put the story
in the commit.

### Cleanup in Hindsight

When applying this rule retroactively from inside a feature branch,
first establish scope by diffing against the parent branch (or trunk)
to identify which commits this branch actually introduced. Then:

- **Commits introduced in this branch** — prompt the user with two
  options: `fixup!` commits with `git rebase --autosquash` to address
  each causal commit at its source, or a single cleanup commit at
  branch tip. User chooses.
- **Commits already in trunk or a parent branch** — default to
  leaving them alone. Do not raise them as cleanup candidates; act
  only on explicit user instruction. If the user opts in, fold the
  cleanup into a single commit at branch tip and do not rewrite trunk
  or parent-branch history.
- **Scope guard** — if cleaning in-branch bleed would touch a
  colleague's in-flight work or expand the branch beyond its stated
  goal, default to staying in lane: protect the project's current
  goal, leave prior bleed alone, and don't introduce new bleed in the
  current change.
