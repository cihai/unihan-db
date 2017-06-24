# -*- coding: utf8 - *-

import os

from appdirs import AppDirs

#: XDG App directory locations
dirs = AppDirs(
    "unihan_db",  # appname
    "cihai team"  # app author
)


if not os.path.exists(dirs.user_data_dir):
    os.makedirs(dirs.user_data_dir)
