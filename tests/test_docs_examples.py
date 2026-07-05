"""Tests for documentation example contracts."""

from __future__ import annotations

import pathlib
import typing as t

import pytest

from .test_example import load_script

if t.TYPE_CHECKING:
    from .types import UnihanOptions


class DocsContentCase(t.NamedTuple):
    """Expected source-level contract for one docs page."""

    test_id: str
    path: pathlib.Path
    required_text: str
    forbidden_text: str


def test_bootstrap_example_forwards_unihan_options(
    monkeypatch: pytest.MonkeyPatch,
    project_root: pathlib.Path,
    unihan_options: UnihanOptions,
) -> None:
    """The literal-included bootstrap example must support offline fixture options."""
    example = load_script("01_bootstrap", project_root=project_root)

    class StopExample(Exception):
        """Stop the example after the bootstrap call is observed."""

    observed: dict[str, object | None] = {}

    def fake_bootstrap_unihan(session: object, options: object | None = None) -> None:
        observed["session"] = session
        observed["options"] = options
        raise StopExample

    monkeypatch.setattr(example.bootstrap, "bootstrap_unihan", fake_bootstrap_unihan)

    with pytest.raises(StopExample):
        example.run(unihan_options)

    assert observed["options"] is unihan_options


DOCS_CONTENT_CASES: tuple[DocsContentCase, ...] = (
    DocsContentCase(
        test_id="homepage-uses-tested-bootstrap-example",
        path=pathlib.Path("docs/index.md"),
        required_text="```{literalinclude} ../examples/01_bootstrap.py",
        forbidden_text="bootstrap_unihan(engine)",
    ),
)


@pytest.mark.parametrize(
    "case",
    DOCS_CONTENT_CASES,
    ids=[case.test_id for case in DOCS_CONTENT_CASES],
)
def test_docs_pages_use_tested_examples(
    project_root: pathlib.Path,
    case: DocsContentCase,
) -> None:
    """Docs pages should reuse tested examples instead of drifting inline snippets."""
    page = project_root / case.path
    source = page.read_text(encoding="utf-8")

    assert case.required_text in source
    assert case.forbidden_text not in source
