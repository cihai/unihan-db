#!/usr/bin/env python
"""Example for bootstrapping UNIHAN DB."""

from __future__ import annotations

import logging
import pprint

from sqlalchemy import func, select

from unihan_db import bootstrap
from unihan_db.tables import Unhn

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def run(unihan_options: dict[str, object] | None = None) -> None:
    """Initialize Unihan DB via ``bootstrap_unihan()``."""
    session = bootstrap.get_session()

    bootstrap.bootstrap_unihan(session)

    random_row = session.execute(
        select(Unhn).order_by(func.random()).limit(1),
    ).scalar_one_or_none()

    assert random_row is not None

    log.info(pprint.pformat(bootstrap.to_dict(random_row)))

    log.info(pprint.pformat(random_row.to_dict()))


if __name__ == "__main__":
    run()
