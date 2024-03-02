"""Typings for unihan-db tests."""

import pathlib
import typing as t


class UnihanOptions(t.TypedDict):
    """Unihan options dictionary."""

    source: pathlib.Path
    work_dir: pathlib.Path
    zip_path: pathlib.Path
