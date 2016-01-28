try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import versioneer

import glob, shutil, os


config = {
    'description': 'Convert python output to reveal.js presentations',
    'author': 'Matt Conley',
    'url': 'https://github.com/mtconley/slipy',
    'download_url': 'https://github.com/mtconley/slipy.git',
    'author_email': None,
    'version': '0.0.1',
    'install_requires': ['IPython', 'mpld3', 'networkx'], 
    'dependency_links': [],
    'packages': find_packages(),
    'scripts': [],
    'name': 'slipy',
}

setup(**config)