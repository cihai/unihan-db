"""Pytest configuration for Unihan DB."""
import pathlib
import typing as t
import zipfile

import pytest
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.scoping import ScopedSession

from unihan_db.bootstrap import UNIHAN_FILES

from .types import UnihanOptions


@pytest.fixture
def tests_path() -> pathlib.Path:
    """Return ``Path`` of tests/."""
    return pathlib.Path(__file__).parent


@pytest.fixture
def fixture_path(tests_path: pathlib.Path) -> pathlib.Path:
    """Return ``Path`` of tests/fixtures/."""
    return tests_path / "fixtures"


@pytest.fixture
def test_config_file(fixture_path: pathlib.Path) -> pathlib.Path:
    """Return ``Path`` to test_config.yml."""
    return fixture_path / "test_config.yml"


@pytest.fixture
def zip_path(tmp_path: pathlib.Path) -> pathlib.Path:
    """Return path to temporary test Unihan.zip."""
    return tmp_path / "Unihan.zip"


@pytest.fixture
def zip_file(zip_path: pathlib.Path, fixture_path: pathlib.Path) -> zipfile.ZipFile:
    """Zip and return archive with ``UNIHAN_FILES``."""
    _files = []
    for f in UNIHAN_FILES:
        _files += [fixture_path / f]
    zf = zipfile.ZipFile(zip_path, "a")
    for _f in _files:
        zf.write(_f, _f.name)
    zf.close()
    return zf


@pytest.fixture
def unihan_options(
    zip_file: zipfile.ZipFile, zip_path: pathlib.Path, tmp_path: pathlib.Path,
) -> "UnihanOptions":
    """Return test ``UnihanOptions``."""
    return {
        "source": zip_path,
        "work_dir": tmp_path,
        "zip_path": tmp_path / "downloads" / "Moo.zip",
    }


@pytest.fixture(scope="function")
def tmpdb_file(tmpdir: pathlib.Path) -> pathlib.Path:
    """Return ``tests.db`` for SQLite."""
    return tmpdir / "test.db"


@pytest.fixture(scope="session")
def engine() -> sqlalchemy.Engine:
    """Return SQLAlchemy engine."""
    return sqlalchemy.create_engine("sqlite:///")


@pytest.fixture(scope="session")
def metadata() -> sqlalchemy.MetaData:
    """Return SQLAlachemy MetaData."""
    return sqlalchemy.MetaData()


@pytest.fixture(scope="function")
def session(
    engine: sqlalchemy.Engine,
    request: pytest.FixtureRequest,
) -> ScopedSession[t.Any]:
    """Return ``ScopedSession``."""
    connection = engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)

    def teardown() -> None:
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
