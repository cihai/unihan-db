(quickstart)=

# Quickstart

## Installation

Assure you have at least python **>= 3.7**.

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

Install into an isolated environment with [pipx] (exposes the `unihan-etl` CLI from dependencies):

```console
$ pipx install 'unihan-db' --include-deps
```

You can upgrade to the latest release with:

```console
$ pip install --upgrade unihan-db
```

(developmental-releases)=

### Developmental releases

New versions of unihan-db are published to PyPI as alpha, beta, or release candidates. In their
versions you will see notification like `a1`, `b1`, and `rc1`, respectively. `1.10.0b4` would mean
the 4th beta release of `1.10.0` before general availability.

- [pip]\:

  ```console
  $ pip install --upgrade --pre unihan-db
  ```

- [pipx]\:

  ```console
  $ pipx install --suffix=@next 'unihan-db' --pip-args '\--pre' --include-deps --force
  // Provides the unihan-etl CLI from the dependency set.
  ```

- [uv]:

  ```console
  $ uv add unihan-db --prerelease allow
  ```

- [uvx]:

  ```console
  $ uvx --from 'unihan-db' --prerelease allow python -c "import unihan_db.bootstrap as bootstrap; print(bootstrap.TABLE_NAME)"
  ```

via trunk (can break easily):

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
[uv]: https://docs.astral.sh/uv/
[uvx]: https://docs.astral.sh/uv/guides/tools/

## Usage

```{literalinclude} ../examples/01_bootstrap.py
:language: python
```

## Pythonics

:::{seealso}

{ref}`unihan-db's API documentation <api>`.
