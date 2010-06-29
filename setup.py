#!/usr/bin/env python

import subprocess

from distutils.core import setup

def get_version():
    version_cmd = 'bin/dodo-version.sh'
    proc = subprocess.Popen(args=version_cmd.split(), stdout=subprocess.PIPE)
    (out, err) = proc.communicate()

    with file('lib/dodo/.version', 'w') as fobj:
        fobj.write(out)

    return out

setup(
    name = 'dodo',
    version = get_version(),
    description = 'Very simple task management tool for a terminal access',

    author = 'Eino Malinen',
    author_email = 'volinthius@sci.fi',

    packages = [ 'dodo' ],
    package_dir = { '': 'lib' },
    package_data = { '': [ '.version' ] },
    scripts = [ 'bin/dodo' ]
    )
