#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'dodo',
    version = '1.0',
    description = 'Very simple task management tool for a terminal access',

    author = 'Eino Malinen',
    author_email = 'volinthius@sci.fi',

    package_dir = { '': 'lib' },
    packages = [ 'dodo' ],
    scripts = [ 'bin/dodo' ]
    )
