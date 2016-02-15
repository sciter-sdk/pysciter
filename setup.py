try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'PySciter',
    'author': 'pravic',
    'author_email': 'ehysta@gmail.com',
    'description': 'Python bindings for the Sciter - Embeddable HTML/CSS/script engine.',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'version': '0.1',
    'packages': ['sciter'],
    'install_requires': ['nose'],
    'scripts': [],
    'keywords': ['gui', 'webkit', 'html', "web"],
    'license': 'MIT',
    'classifiers': [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: GTK',
        'Environment :: X11 Applications :: Qt',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
    ],
}

setup(**config)
