import os
import pathlib
import typing as t
import zipfile

import pytest

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.schema import MetaData

from unihan_db.bootstrap import UNIHAN_FILES


@pytest.fixture
def fixture_path() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "fixtures"))


@pytest.fixture
def test_config_file(fixture_path: pathlib.Path) -> pathlib.Path:
    return fixture_path / "test_config.yml"


@pytest.fixture
def zip_path(tmpdir: pathlib.Path) -> pathlib.Path:
    return tmpdir / "Unihan.zip"


@pytest.fixture
def zip_file(zip_path: pathlib.Path, fixture_path: pathlib.Path) -> zipfile.ZipFile:
    _files = []
    for f in UNIHAN_FILES:
        _files += [os.path.join(fixture_path, f)]
    zf = zipfile.ZipFile(str(zip_path), "a")
    for f in _files:
        zf.write(f, os.path.basename(f))
    zf.close()
    return zf


class UnihanTestOptions(t.TypedDict):
    source: pathlib.Path
    work_dir: pathlib.Path
    zip_path: pathlib.Path
    expand: bool


@pytest.fixture
def unihan_options(
    zip_file: pathlib.Path, zip_path: pathlib.Path, tmp_path: pathlib.Path
) -> UnihanTestOptions:
    return {
        "source": zip_path,
        "work_dir": tmp_path,
        "zip_path": tmp_path / "downloads" / "Moo.zip",
        "expand": True,
    }


@pytest.fixture(scope="function")
def tmpdb_file(tmp_path: pathlib.Path) -> pathlib.Path:
    return tmp_path / "test.db"


@pytest.fixture
def engine() -> Engine:
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="function")
def session(engine: Engine, request: pytest.FixtureRequest) -> ScopedSession:
    connection = engine.connect()
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)

    def teardown() -> None:
        connection.close()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def metadata(engine: Engine) -> MetaData:
    metadata = MetaData(bind=engine)
    return metadata
