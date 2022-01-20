#!/usr/bin/env python
import sys
import wialon

from setuptools import setup, find_packages


extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True
    extra['convert_2to3_doctests'] = ['README.md']

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
    ]

KEYWORDS = 'async wialon remote api wrapper'

setup(name='py-aiowialon',
      version=wialon.__version__,
      description="""Wialon Remote API wrapper for Python.""",
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      author=wialon.__author__,
      url='https://github.com/o-murphy/py-aiowialon',
      packages=find_packages(),
      download_url='http://pypi.python.org/pypi/py-aiowialon/',
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      zip_safe=True,
      install_requires=['simplejson', 'future', 'aiohttp'],
      py_modules=['py-aiowialon']
      )
