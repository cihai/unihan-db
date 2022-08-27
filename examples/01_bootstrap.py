#!/usr/bin/env python
import pprint

from sqlalchemy.sql.expression import func

from unihan_db import bootstrap
from unihan_db.tables import Unhn

session = bootstrap.get_session()

bootstrap.bootstrap_unihan(session)

random_row = session.query(Unhn).order_by(func.random()).limit(1).first()

assert random_row is not None

pprint.pprint(bootstrap.to_dict(random_row))
