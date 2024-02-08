"""Test examples/ found in cihai source directory."""
import importlib
import importlib.util
import pathlib
import sys
import types
import typing as t

if t.TYPE_CHECKING:
    from .types import UnihanOptions


class LoadScriptFn(t.Protocol):
    """Protocol typings for load_script()."""

    def __callable__(
        self,
        example: str,
        project_root: pathlib.Path,
    ) -> types.ModuleType:
        """Return script as a module."""
        ...


def load_script(example: str, project_root: pathlib.Path) -> types.ModuleType:
    """Load script as module via name and project root."""
    file_path = f"{project_root}/examples/{example}.py"
    module_name = "run"

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    assert spec.loader is not None
    spec.loader.exec_module(module)

    return module


def test_01_bootstrap(
    unihan_options: "UnihanOptions",
    project_root: pathlib.Path,
) -> None:
    """Test example dataset."""
    example = load_script("01_bootstrap", project_root=project_root)
    example.run()
