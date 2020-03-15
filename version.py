"""
Gets the current version number from the file version.txt (which is created during the build process).

To use this script, simply import it in your setup.py file
and use the results of get_version() as your package version:

    from version import *

    setup(
        ...
        version=get_version(),
        ...
    )
"""

__all__ = 'get_version'

from os.path import dirname, exists, join


def get_version():
    version = "0.0.0"  # default if version.txt does not exist
    # Extract the version from the version.txt file
    version_file: str = join(dirname(__file__), 'version.txt')
    if exists(version_file):
        with open(version_file) as f:
            version = f.read()
    return version


if __name__ == '__main__':
    print(get_version())
