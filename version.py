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

from os.path import dirname, join


def get_version():
    # Extract the version from the PKG-INFO file.
    d = dirname(__file__)
    with open(join(d, 'version.txt')) as f:
        version = f.read()

    return version


if __name__ == '__main__':
    print(get_version())