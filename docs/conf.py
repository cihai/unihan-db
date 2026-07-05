"""Sphinx documentation configuration for unihan-db."""

from __future__ import annotations

import doctest
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
    extra_extensions=["sphinx.ext.doctest", "sphinx_autodoc_api_style"],
    intersphinx_mapping={
        "python": ("https://docs.python.org/3/", None),
        "sqlalchemy": ("https://docs.sqlalchemy.org/en/21/", None),
    },
    linkcode_resolve=make_linkcode_resolve(unihan_db, about["__github__"]),
    html_favicon="_static/favicon.ico",
    html_extra_path=["manifest.json"],
    rediraffe_redirects="redirects.txt",
    # AGENTS.md is agent guidance, not a site page; keep Sphinx from
    # treating it as an orphan document.
    exclude_patterns=["_build", "AGENTS.md", "CLAUDE.md"],
)
globals().update(conf)

doctest_default_flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
doctest_global_setup = """
import os
import pathlib
import tempfile

_doctest_tmpdir = tempfile.TemporaryDirectory()
tmp_path = pathlib.Path(_doctest_tmpdir.name)
_doctest_old_home = os.environ.get("HOME")
_doctest_old_cwd = pathlib.Path.cwd()
os.environ["HOME"] = str(tmp_path)
os.chdir(tmp_path)
"""
doctest_global_cleanup = """
os.chdir(_doctest_old_cwd)
if _doctest_old_home is None:
    os.environ.pop("HOME", None)
else:
    os.environ["HOME"] = _doctest_old_home
_doctest_tmpdir.cleanup()
"""
