# Contributing

Thanks for looking. unihan-db is pre-1.0, so a bug report with a
reproduction, or a pull request that fixes one verified problem, is the most
useful thing right now.

How this project writes prose — README, `CHANGES`, commit messages,
docstrings, and source comments — is set out separately in
[WRITING.md](WRITING.md). Read that before changing any of it. The
constraints every change is held to, and the map of what is where, are in
[AGENTS.md](../AGENTS.md).

unihan-db also follows the
[cihai contributing guide](https://cihai.git-pull.com/project/contributing/)
for conventions shared across the cihai family — the same `pytest`,
`sphinx`, `mypy`, `ruff`, and `tmuxp` tooling applies there too.

## Getting set up

```console
$ uv sync --all-extras --dev
```

`just --list` shows every available command, including file watchers
(`just watch-ruff`, `just watch-mypy`, `just watch-docs`) that need
[`entr`](https://eradman.com/entrproject/).

## The gates

Format:

```console
$ uv run ruff format .
```

Lint:

```console
$ uv run ruff check . --fix --show-fixes
```

Type-check (`[tool.mypy]` runs in strict mode):

```console
$ uv run mypy .
```

Test:

```console
$ uv run pytest
```

Documentation is a gate, not a courtesy. Examples in docstrings and
documentation pages are executed by `pytest`; the doctest flags live in
`pyproject.toml`, so there is no separate doctest step and a green `pytest`
is the proof. Which blocks qualify, and the one mistake that silently
removes a test, are in
[WRITING.md](WRITING.md#documented-examples-that-run).

Before claiming a test or a gate works, show it failing. A gate that has
never been red is an assumption.

CI (`.github/workflows/tests.yml`) runs `ruff check .`, `ruff format .
--check`, `mypy .`, and `pytest --cov=./ --cov-report=xml` against Python
3.10 and 3.14 on every push and pull request. It is the order of record —
match it exactly before you call a change done.

### Import conventions

Every module starts with `from __future__ import annotations` — ruff's
isort rule (`required-imports` in `pyproject.toml`) adds it automatically on
`ruff check . --fix`, so this is enforced, not a style reminder. Import the
standard library through a namespace (`import typing as t`) rather than
`from typing import X`; third-party packages may use `from X import Y`.

## Tests

Tests never touch the network. `bootstrap_unihan()` against real UNIHAN data
downloads from unicode.org; the suite instead zips the fixture files under
`tests/fixtures/` and points `unihan_options` at the zip, so the importer
sees the same shape of data offline.

Prefer these fixtures over ad-hoc setup — all in `tests/conftest.py`
except `project_root`, which is in the root `conftest.py`:

| Fixture          | Provides                                        |
| ---------------- | ------------------------------------------------ |
| `engine`         | session-scoped in-memory SQLite `Engine`          |
| `session`        | a `ScopedSession` inside a rolled-back transaction |
| `unihan_options` | ETL options pointed at the zipped fixture data    |
| `zip_file`       | the zipped `UNIHAN_FILES` fixture archive         |
| `project_root`   | the repository root, for loading `examples/`      |

The root `conftest.py`'s autouse fixtures set `HOME` and the working
directory to a fresh temporary path for every test and doctest, so a test
can write files without touching a real home directory. If you add a
doctest, it inherits this automatically — see
[WRITING.md](WRITING.md#documented-examples-that-run) for what a doctest may
assume.

`pytest-rerunfailures` is installed, but `addopts` sets `--reruns=0` — a red
test is red, not flaky. Do not silence a failure by asking for a rerun.

**Debugging.** `bootstrap`'s logger defaults to `INFO`, which already
streams download and import progress — reach for that instead of adding
`print()`. If ORM objects look stale mid-test, recreate the session or
re-run `Base.metadata.create_all()` against the test engine rather than
reusing state across tests.

`examples/01_bootstrap.py` is exercised directly by `tests/test_example.py`,
and `tests/test_docs_examples.py` asserts that `docs/index.md` embeds that
same script via `{literalinclude}` rather than a hand-copied snippet that
could drift out of sync.

## Documentation

```console
$ just build-docs
```

builds the HTML site (`docs/justfile html`) and then runs the Sphinx
doctest builder (`docs/justfile doctest`) against every
```` ```{doctest} ```` block under `docs/`. Requires
[`just`](https://just.systems/) in addition to `uv`.

`docs/api/*.md` are hand-written pages that call `.. automodule::` — edit
them directly; nothing under `docs/` is generated. `docs/_build/` is build
output and is gitignored.

`docs/redirects.txt` feeds the `rediraffe` extension. After renaming or
removing a documentation page, regenerate the diff instead of hand-editing
guesses:

```console
$ just -f docs/justfile redirects
```

## Releasing

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow. See
[Release commits](WRITING.md#release-commits).

unihan-db is pre-1.0: APIs may change between minor versions. To cut a
release, update `CHANGES` with the new version and date, bump the version in
`src/unihan_db/__about__.py` and `pyproject.toml`, commit, then tag
`v<version>` and push the tag. The tag push triggers
`.github/workflows/tests.yml`'s `release` job, which builds the package and
publishes to PyPI over trusted publishing (OIDC) — there is no separate
manual upload step. Full checklist:
[docs/project/releasing.md](https://github.com/cihai/unihan-db/blob/master/docs/project/releasing.md).

## Pull requests

One subject per pull request. Unrelated cleanup found along the way belongs
in its own commit, and usually in its own pull request.

Discuss a substantial change via an issue before making it.

Commit format is in [WRITING.md](WRITING.md#commits).

You may merge the pull request once you have the sign-off of one other
developer. If you do not have permission to do that, you may request a
reviewer to merge it for you.

## Decorum

- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of
  personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should
  always assume good intentions.
- Behaviour which can be reasonably considered harassment will not be
  tolerated.

Based on
[Ruby's Community Conduct Guideline](https://www.ruby-lang.org/en/conduct/).

## Security

Please do not open a public issue for a vulnerability. Report it through
[GitHub's private vulnerability reporting](https://github.com/cihai/unihan-db/security/advisories/new)
for this repository.
