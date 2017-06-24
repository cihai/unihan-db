#!/usr/bin/env python
# -*- coding: utf8 - *-
from __future__ import (absolute_import, print_function, unicode_literals,
                        with_statement)

import random

from sqlalchemy.orm import joinedload

from unihan_db import bootstrap
from unihan_db.tables import Unhn

# If using postgres, example:
# session = bootstrap.get_session(
#     'postgresql://postgres:postgres@localhost/unihan_db'
# )

session = bootstrap.get_session()

bootstrap.bootstrap_unihan(session)

row_count = session.query(Unhn).count()


def random_row():
    return random.randrange(row_count)


print(random_row())
random_row = session.query(Unhn).options(joinedload('kDefinition')).offset(
    random_row()
).limit(1).first()

print(random_row.to_dict())
