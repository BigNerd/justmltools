# This program is placed into the public domain.
# Source: https://gist.github.com/pwithnall/7bc5f320b3bdf418265a

"""
Gets the current version number.
If in a git repository, it is the current git tag.

If the current commit is not tagged, the version is the tag of the last tagged ancestor commit
plus a suffix .post<n>, where <n> is the number of commits after the last tagged ancestor commit.

If the git repository has uncommitted changes in addition to the last commit, another suffix .dev1 is appended, too.

In not in a git repo, the version is the one contained in the PKG-INFO file (if it exists).

To use this script, simply import it in your setup.py file
and use the results of get_version() as your package version:

    from version import *

    setup(
        ...
        version=get_version(),
        ...
    )
"""

__all__ = ('get_version')

from os.path import dirname, exists, isdir, join
import os
import re
import subprocess

version_re = re.compile('^Version: (.+)$', re.M)


def get_version():
    d = dirname(__file__)

    if isdir(join(d, '.git')):
        # Get the version using "git describe".
        cmd = 'git describe --tags --match [0-9]*'.split()
        try:
            version = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            print('Unable to get version number from git tags')
            exit(1)

        # PEP 386 compatibility
        if '-' in version:
            version = '.post'.join(version.split('-')[:2])

        # Don't declare a version "dirty" merely because a time stamp has
        # changed. If it is dirty, append a ".dev1" suffix to indicate a
        # development revision after the release.
        with open(os.devnull, 'w') as fd_devnull:
            subprocess.call(['git', 'status'],
                            stdout=fd_devnull, stderr=fd_devnull)

        cmd = 'git diff-index --name-only HEAD'.split()
        try:
            dirty = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            print('Unable to get git index status')
            exit(1)

        if dirty != '':
            version += '.dev1'

    else:
        # Extract the version from the PKG-INFO file.
        with open(join(d, 'PKG-INFO')) as f:
            version = version_re.search(f.read()).group(1)

    return version


if __name__ == '__main__':
    print(get_version())





