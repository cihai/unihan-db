# AGENTS.md

Logging conventions for `src/unihan_db/**`. These rules guide future
logging changes; existing code may not yet conform. Everything else about
how this package is written — docstrings, comments, commits — is in
[../../.github/WRITING.md](../../.github/WRITING.md); this file only covers
log calls.

## Logger setup

- Use `logging.getLogger(__name__)` in every module.
- Add `NullHandler` in library `__init__.py` files.
- Never configure handlers, levels, or formatters in library code — that is
  the application's job.

## Structured context via `extra`

Pass structured data on every log call where useful for filtering,
searching, or test assertions.

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

Treat established keys as compatibility-sensitive — downstream users may
build dashboards and alerts on them. Change deliberately.

## Key naming rules

- `snake_case`, not dotted; `unihan_` prefix.
- Prefer stable scalars; avoid ad-hoc objects.
- Heavy keys (`unihan_stdout`, `unihan_stderr`) are DEBUG-only; consider
  companion `unihan_stdout_len` fields or hard truncation (e.g.
  `stdout[:100]`).

## Lazy formatting

`logger.debug("msg %s", val)`, not f-strings. Two rationales:

- Deferred string interpolation: skipped entirely when the level is
  filtered.
- Aggregator message template grouping: `"Running %s"` is one signature
  grouped ×10,000; f-strings make each line unique.

When computing `val` itself is expensive, guard with
`if logger.isEnabledFor(logging.DEBUG)`.

## `stacklevel` for wrappers

Increment for each wrapper layer so `%(filename)s:%(lineno)d` and OTel
`code.filepath` point to the real caller. Verify whenever call depth
changes.

## `LoggerAdapter` for persistent context

For objects with stable identity (Dataset, Reader, Exporter), use
`LoggerAdapter` to avoid repeating the same `extra` on every call. Lead with
the portable pattern (override `process()` to merge); `merge_extra=True`
simplifies this on Python 3.13+.

## Log levels

| Level | Use for | Examples |
|-------|---------|----------|
| `DEBUG` | Internal mechanics, data I/O | Field parsing, record transformation steps |
| `INFO` | Data lifecycle, user-visible operations | Download completed, export finished, database bootstrapped |
| `WARNING` | Recoverable issues, deprecation, user-actionable config | Missing optional field, deprecated data format |
| `ERROR` | Failures that stop an operation | Download failed, parse error, database write failed |

Config discovery noise belongs in `DEBUG`; only surprising/user-actionable
config issues go to `WARNING`.

## Message style

- Lowercase, past tense for events: `"download completed"`, `"parse
  error"`.
- No trailing punctuation.
- Keep messages short; put details in `extra`, not the message string.

## Exception logging

- Use `logger.exception()` only inside `except` blocks when you are **not**
  re-raising.
- Use `logger.error(..., exc_info=True)` when you need the traceback
  outside an `except` block.
- Avoid `logger.exception()` followed by `raise` — this duplicates the
  traceback. Either add context via `extra` that would otherwise be lost, or
  let the exception propagate.

## Testing logs

Assert on `caplog.records` attributes, not string matching on
`caplog.text`:

- Scope capture: `caplog.at_level(logging.DEBUG,
  logger="unihan_db.bootstrap")`.
- Filter records rather than index by position: `[r for r in caplog.records
  if hasattr(r, "unihan_field")]`.
- Assert on schema: `record.unihan_record_count == 100`, not `"100
  records" in caplog.text`.
- `caplog.record_tuples` cannot access extra fields — always use
  `caplog.records`.

## Avoid

- f-strings/`.format()` in log calls.
- Unguarded logging in hot loops (guard with `isEnabledFor()`).
- Catch-log-reraise without adding new context.
- `print()` for diagnostics.
- Logging secret env var values (log key names only).
- Non-scalar ad-hoc objects in `extra`.
- Requiring custom `extra` fields in format strings without safe defaults
  (missing keys raise `KeyError`).
