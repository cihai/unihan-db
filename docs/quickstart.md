(quickstart)=

# Quickstart

unihan-db turns [UNIHAN] into local [SQLAlchemy](https://www.sqlalchemy.org/)
tables. For the common path, create a session with
{func}`unihan_db.bootstrap.get_session`, load the data once with
{func}`unihan_db.bootstrap.bootstrap_unihan`, and query
{class}`unihan_db.tables.Unhn` or its related tables. The first bootstrap
downloads and imports the archive; after that, your queries use local [SQLite].

## Installation

Use [Python] **>=3.10,<4.0**.

Using [pip]:

```console
$ pip install unihan-db
```

Inside a project managed by [uv]:

```console
$ uv add unihan-db
```

Run code without installing by using [uvx]:

```console
$ uvx --from unihan-db python -c "import unihan_db.bootstrap as bootstrap; print(bootstrap.TABLE_NAME)"
```

Install into an isolated environment with [pipx]:

```console
$ pipx install 'unihan-db' --include-deps
```

The dependency set includes the [unihan-etl] CLI.

You can upgrade to the latest release with:

```console
$ pip install --upgrade unihan-db
```

## Usage

The example creates a session, runs the bootstrap, queries a random
{class}`~unihan_db.tables.Unhn` row, and shows both
{func}`unihan_db.bootstrap.to_dict` and the row's injected `to_dict()` helper.
For the API details behind those helpers, see
{ref}`unihan-db's API documentation <api>`.

```{literalinclude} ../examples/01_bootstrap.py
:language: python
```

(developmental-releases)=

## Developmental releases

New versions of unihan-db are published to [PyPI] as alpha, beta, or release
candidates. Version suffixes such as `a1`, `b1`, and `rc1` mark those
pre-release stages; `1.10.0b4` is the fourth beta before general availability.

- [pip]\:

  ```console
  $ pip install --upgrade --pre unihan-db
  ```

- [pipx]\:

  ```console
  $ pipx install --suffix=@next 'unihan-db' --pip-args '\--pre' --include-deps --force
  ```

  This also installs the [unihan-etl] CLI from the dependency set.

- [uv]:

  ```console
  $ uv add unihan-db --prerelease allow
  ```

- [uvx]:

  ```console
  $ uvx --from 'unihan-db' --prerelease allow python -c "import unihan_db.bootstrap as bootstrap; print(bootstrap.TABLE_NAME)"
  ```

Install from unreleased `master` only when you need a change that is not on
[PyPI] yet. This follows the current development branch, so APIs and behavior
can change before the next release:

- [pip]\:

  ```console
  $ pip install -e git+https://github.com/cihai/unihan-db.git#egg=unihan-db
  ```

- [uv]:

  ```console
  $ uv add git+https://github.com/cihai/unihan-db.git#egg=unihan-db
  ```

- [pipx]\:

  ```console
  $ pipx install --suffix=@master 'unihan-db @ git+https://github.com/cihai/unihan-db.git@master' --include-deps --force
  ```

[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pypa.github.io/pipx/docs/
[PyPI]: https://pypi.org/
[Python]: https://www.python.org/
[SQLite]: https://www.sqlite.org/
[UNIHAN]: https://www.unicode.org/charts/unihan.html
[unihan-etl]: https://unihan-etl.git-pull.com/
[uv]: https://docs.astral.sh/uv/
[uvx]: https://docs.astral.sh/uv/guides/tools/
