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

## Debugging Tips

- When ETL runs slowly, log level INFO in `bootstrap` already streams progress; avoid adding noisy prints.
- If objects look stale, recreate sessions or re-run `Base.metadata.create_all` against your engine in tests.
- Use the provided fixtures to keep paths isolated—tests assume `HOME` and cwd are temporary.

## gp-libs/cihai References

- Docs: https://unihan-db.git-pull.com/
- API: https://unihan-db.git-pull.com/api.html
- Dataset: https://www.unicode.org/charts/unihan.html
- unihan-etl: https://unihan-etl.git-pull.com
