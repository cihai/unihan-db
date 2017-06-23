#!/usr/bin/env python
# -*- coding: utf8 - *-
from __future__ import (absolute_import, print_function, unicode_literals,
                        with_statement)

from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import func

from unihan_db import bootstrap
from unihan_db.tables import Unhn

# If using postgres, example:
# session = bootstrap.get_session(
#     'postgresql://postgres:postgres@localhost/unihan_db'
# )

session = bootstrap.get_session()

bootstrap.bootstrap_unihan(session)

random_row = session.query(Unhn).options(joinedload('kDefinition')).filter(
    Unhn.kDefinition != None  # noqa
).order_by(func.random()).first()

print(random_row.to_dict())
