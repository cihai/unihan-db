(code-style)=

# Code style

## Linting and formatting

unihan-db uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting.

Lint the codebase:

```console
$ uv run ruff check . --fix --show-fixes
```

Format the codebase:

```console
$ uv run ruff format .
```

## Type checking

[mypy](https://github.com/python/mypy) is configured in strict mode.

```console
$ uv run mypy src tests
```

## Conventions

- `from __future__ import annotations` in every module.
- Namespace imports for stdlib: `import typing as t`.
- NumPy-style docstrings.
- See `[tool.ruff]` in `pyproject.toml` for the full rule set.
