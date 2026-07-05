(offline-bootstrap)=

# Bootstrap from a Local Archive

{func}`unihan_db.bootstrap.bootstrap_unihan` accepts the same ETL options as
{func}`unihan_db.bootstrap.bootstrap_data`. Pass a local `source` archive when
you need deterministic tests, offline development, or a pre-downloaded UNIHAN
zip.

The repository tests use this path: `tests/conftest.py` builds a local archive
from `tests/fixtures/`, then passes `source`, `work_dir`, and `zip_path` through
the `unihan_options` fixture. That keeps bootstrap coverage offline while still
exercising the real importer.

Use the default options for normal applications. The default path downloads the
current UNIHAN archive through
[unihan-etl](https://unihan-etl.git-pull.com/) and then reuses the local
database on later runs.
