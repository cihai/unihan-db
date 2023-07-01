from appdirs import AppDirs as BaseAppDirs

from unihan_etl._internal.app_dirs import AppDirs

#: XDG App directory locations
dirs = AppDirs(_app_dirs=BaseAppDirs("unihan_db", "cihai team"))


if not dirs.user_data_dir.exists():
    dirs.user_data_dir.mkdir(parents=True)
