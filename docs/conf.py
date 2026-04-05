"""Sphinx documentation configuration for unihan-db."""

from __future__ import annotations

import pathlib
import sys

from gp_sphinx.config import make_linkcode_resolve, merge_sphinx_config

import unihan_db

# Get the project root dir, which is the parent dir of this
cwd = pathlib.Path(__file__).parent
project_root = cwd.parent
src_root = project_root / "src"

sys.path.insert(0, str(src_root))

# package data
about: dict[str, str] = {}
with (src_root / "unihan_db" / "__about__.py").open() as fp:
    exec(fp.read(), about)

conf = merge_sphinx_config(
    project=about["__title__"],
    version=about["__version__"],
    copyright=about["__copyright__"],
    source_repository=f"{about['__github__']}/",
    docs_url=about["__docs__"],
    source_branch="master",
    light_logo="img/cihai.svg",
    dark_logo="img/cihai.svg",
    intersphinx_mapping={
        "python": ("http://docs.python.org/3/", None),
        "sqlalchemy": ("http://docs.sqlalchemy.org/en/latest/", None),
    },
    linkcode_resolve=make_linkcode_resolve(unihan_db, about["__github__"]),
    html_favicon="_static/favicon.ico",
    html_extra_path=["manifest.json"],
    rediraffe_redirects="redirects.txt",
)
globals().update(conf)
