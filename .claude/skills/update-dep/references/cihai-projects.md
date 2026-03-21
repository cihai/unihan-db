# cihai Ecosystem Reference

Known packages, local clone paths, and documentation URLs for the cihai
project family.

## Dependency Graph

```
cihai-cli -> cihai -> unihan-etl
unihan-db -> unihan-etl
```

## Packages

### unihan-etl

| Property | Value |
|----------|-------|
| PyPI | `unihan-etl` |
| Module | `unihan_etl` |
| GitHub | `cihai/unihan-etl` |
| Docs | `https://unihan-etl.git-pull.com` |
| History | `https://unihan-etl.git-pull.com/history.html` |
| Local clone | `~/work/cihai/unihan-etl` |
| Tag format | `v<version>` (e.g., `v0.41.0`) |

### unihan-db

| Property | Value |
|----------|-------|
| PyPI | `unihan-db` |
| Module | `unihan_db` |
| GitHub | `cihai/unihan-db` |
| Docs | `https://unihan-db.git-pull.com` |
| History | `https://unihan-db.git-pull.com/history.html` |
| Local clone | `~/work/cihai/unihan-db` |

### cihai

| Property | Value |
|----------|-------|
| PyPI | `cihai` |
| Module | `cihai` |
| GitHub | `cihai/cihai` |
| Docs | `https://cihai.git-pull.com` |
| History | `https://cihai.git-pull.com/history.html` |
| Local clone | `~/work/cihai/cihai` |

### cihai-cli

| Property | Value |
|----------|-------|
| PyPI | `cihai-cli` |
| Module | `cihai_cli` |
| GitHub | `cihai/cihai-cli` |
| Docs | `https://cihai-cli.git-pull.com` |
| History | `https://cihai-cli.git-pull.com/history.html` |
| Local clone | `~/work/cihai/cihai-cli` |

## CHANGES Anchor Construction

Two URL patterns are used in `See also:` links. Both are derived from the
version heading in the upstream CHANGES file.

### Source heading example

```
## unihan-etl 0.39.1 (2026-01-24)
```

### GitHub anchor

Dots are stripped from the version number.

```
unihan-etl-0391-2026-01-24
```

Full URL:

```
https://github.com/cihai/unihan-etl/blob/v0.39.1/CHANGES#unihan-etl-0391-2026-01-24
```

### Docs anchor

Dots become hyphens in the version number.

```
unihan-etl-0-39-1-2026-01-24
```

Full URL:

```
https://unihan-etl.git-pull.com/history.html#unihan-etl-0-39-1-2026-01-24
```

## API Surface: unihan-etl in unihan-db

These are the import sites to check when updating unihan-etl:

| File | Import | Risk |
|------|--------|------|
| `src/unihan_db/__init__.py` | `from unihan_etl._internal.app_dirs import AppDirs` | High (internal API) |
| `src/unihan_db/bootstrap.py` | `from unihan_etl import core as unihan` | Medium (core Packager) |
| `src/unihan_db/bootstrap.py` | `from unihan_etl.util import merge_dict` | Low (stable utility) |
| `src/unihan_db/bootstrap.py` | `from unihan_etl.types import UntypedNormalizedData, UntypedUnihanData` | Low (type aliases) |
| `src/unihan_db/importer.py` | `from unihan_etl.expansion import kRSSimplifiedType` | Medium (data enum) |
| `tests/fixtures/Unihan_*.txt` | Copied from unihan-etl test data | Changes with UNIHAN revisions |

## Downstream Propagation

After updating unihan-etl in unihan-db, the same update should typically be
applied to:

1. `cihai` (depends on unihan-etl directly)
2. `cihai-cli` (depends on cihai, inherits transitively)

These are separate PRs in their respective repositories.
