#!/usr/bin/env python
"""Example for bootstrapping UNIHAN DB."""
import pprint

from sqlalchemy.sql.expression import func
from unihan_db import bootstrap
from unihan_db.tables import Unhn

session = bootstrap.get_session()

bootstrap.bootstrap_unihan(session)

random_row_query = session.query(Unhn).order_by(func.random()).limit(1)

assert random_row_query is not None

random_row = random_row_query.first()

pprint.pprint(bootstrap.to_dict(random_row))

pprint.pprint(random_row.to_dict())  # type:ignore
