#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'PySciter',
    'author': 'pravic',
    'author_email': 'ehysta@gmail.com',
    'description': 'Python bindings for the Sciter - Embeddable HTML/CSS/script engine (cross-platform desktop GUI toolkit).',
    'url': 'https://github.com/sciter-sdk/pysciter/',
    'download_url': 'https://github.com/sciter-sdk/pysciter/releases',
    'bugtrack_url': 'https://github.com/sciter-sdk/pysciter/issues',
    'version': '0.6.4',
    'platforms': ['Windows', 'Linux', 'MacOS X', ],
    'packages': ['sciter', 'sciter.capi'],
    'install_requires': [''],
    'scripts': [],
    'keywords': ['gui', 'sciter', 'javascript', 'tiscript', 'htmlayout', 'html', 'css', 'web', 'cross-platform', ],
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows :: Windows XP',
        'Operating System :: Microsoft :: Windows :: Windows Vista',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: GTK',
        'Environment :: Web Environment',
        'Programming Language :: C++',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Widget Sets',
    ],
    'long_description': """
Introduction
============
Sciter (https://sciter.com) is an embeddable HTML/CSS/script engine with GPU accelerated rendering for desktop application UI.
It's a compact, single dll/dylib/so file (4-8 mb), engine without any additional dependencies.

Sciter uses Direct2D GPU accelerated graphics on modern Windows versions and GDI+ on XP.
On OS X, it uses standard CoreGraphics primitives, while the Linux version uses Cairo.

Sciter uses HTML5 set of elements, implements CSS level 2.1 in full, plus the most popular features of CSS level 3.
It also contains custom CSS extensions that are required to support desktop UI cases.
For example, flex units and various layout managers.

Check the `screenshot gallery <https://github.com/oskca/sciter#sciter-desktop-ui-examples>`_ of the desktop UI examples.


Installation
============

For installation instructions and usage examples please refer to `github project page <https://github.com/sciter-sdk/pysciter#getting-started>`_.


Compatibility
=============

PySciter requires Python 3.x.

Sciter works on:

- Microsoft Windows XP and above (x86/x64)
- macOS v 10.7 and above (64-bit)
- Linux/GTK (GTK v 3.0 and above, 64-bit only)
- Raspberry Pi


Feedback and getting involved
=============================
- PySciter Code Repository: https://github.com/sciter-sdk/pysciter
- Issue tracker: https://github.com/sciter-sdk/pysciter/issues
- Sciter official website: https://sciter.com
- Sciter forum: https://sciter.com/forums/
- Sciter SDK: https://github.com/c-smile/sciter-sdk

""",
}

setup(**config)
