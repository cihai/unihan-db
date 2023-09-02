(quickstart)=

# Quickstart

## Installation

Assure you have at least python **>= 3.7**.

```console
$ pip install unihan-db
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

via trunk (can break easily):

- [pip]\:

  ```console
  $ pip install -e git+https://github.com/cihai/unihan-db.git#egg=unihan-db
  ```

[pip]: https://pip.pypa.io/en/stable/

## Usage

```{literalinclude} ../examples/01_bootstrap.py
:language: python
```

## Pythonics

:::{seealso}

{ref}`unihan-db's API documentation <api>`.
