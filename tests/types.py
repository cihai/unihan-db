"""Typings for unihan-db tests."""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    import pathlib


class UnihanOptions(t.TypedDict):
    """Unihan options dictionary."""

    source: pathlib.Path
    work_dir: pathlib.Path
    zip_path: pathlib.Path
