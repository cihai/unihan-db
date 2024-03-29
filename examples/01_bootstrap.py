#!/usr/bin/env python
"""Example for bootstrapping UNIHAN DB."""

import pprint
import typing as t

from sqlalchemy.sql.expression import func

from unihan_db import bootstrap
from unihan_db.tables import Unhn


def run(unihan_options: t.Optional[t.Dict[str, object]] = None) -> None:
    """Initialize Unihan DB via ``bootstrap_unihan()``."""
    session = bootstrap.get_session()

    bootstrap.bootstrap_unihan(session)

    random_row_query = session.query(Unhn).order_by(func.random()).limit(1)

    assert random_row_query is not None

    random_row = random_row_query.first()

    pprint.pprint(bootstrap.to_dict(random_row))

    assert random_row is not None

    pprint.pprint(random_row.to_dict())  # type:ignore


if __name__ == "__main__":
    run()
