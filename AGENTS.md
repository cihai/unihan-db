# AGENTS.md

unihan-db packages SQLAlchemy ORM models and bootstrap helpers that load the
Unicode UNIHAN CJK character dataset into a local database, via
[unihan-etl](https://unihan-etl.git-pull.com). Part of the
[cihai](https://cihai.git-pull.com) project family.

Follow the conventions already in the tree, and keep a change scoped to what
was asked for.

## What is here

| Path | What it is |
| ---- | ---------- |
| `src/unihan_db/bootstrap.py` | Session/engine setup, `bootstrap_unihan()`, `to_dict()` |
| `src/unihan_db/importer.py` | Normalized UNIHAN records to ORM rows |
| `src/unihan_db/tables.py` | SQLAlchemy ORM schema (`Base`, `Unhn`, and related tables) |
| `src/unihan_db/AGENTS.md` | Logging conventions for this package |
| `examples/01_bootstrap.py` | The bootstrap example embedded in docs and README |
| `tests/` | pytest suite; `tests/fixtures/` holds the offline UNIHAN archive |
| `docs/` | Sphinx site (MyST); `docs/project/` covers contributing and releasing |
| `CHANGES` | Changelog, rendered as the docs changelog page |

## Which policy applies

- Documentation, user-facing text, `CHANGES`, commit messages, docstrings,
  and source comments: [.github/WRITING.md](.github/WRITING.md)
- Environment, the gates, tests, documentation builds, releases, and pull
  requests: [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)
- Logging calls: [src/unihan_db/AGENTS.md](src/unihan_db/AGENTS.md)

Each of those is the single home for its subject. Where a rule seems to be
stated twice, the file listed above is the one that governs.

## Change discipline

- Make the smallest coherent change that solves the verified problem; keep
  unrelated cleanup out of it.
- Reuse an existing file, helper, API, or test before adding a new one.
- Add a file only for a durable boundary — a distinct responsibility,
  independent reuse, or splitting an oversized module — not for a
  single-use helper or a one-line re-export.
- Add a test for every user-visible behaviour change, and a `CHANGES` entry
  for every change to the public API or ORM schema.
- A passing gate is evidence only once it has been shown capable of
  failing. Pair a new test with a deliberate break that proves it bites.

Tests run offline: a real `bootstrap_unihan()` downloads from unicode.org,
so the suite zips the fixtures under `tests/fixtures/` instead — never add a
test that needs network access. The default database is SQLite in the
user's XDG data directory (`unihan_db.dirs`); do not hard-code a path.

## References

- Changelog: [CHANGES](CHANGES)
- Docs: https://unihan-db.git-pull.com/
- API reference: https://unihan-db.git-pull.com/api/
- unihan-etl, the ETL pipeline this package loads from:
  https://unihan-etl.git-pull.com
- cihai, end-user character lookups built on this schema:
  https://cihai.git-pull.com
- UNIHAN dataset: https://www.unicode.org/charts/unihan.html
