from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys
import re

here = os.path.abspath(os.path.dirname(__file__))

def get_tag(tag_name):
    with open(os.path.join(here, '__init__.py'), 'rb') as init_py:
        src = init_py.read().decode('utf-8')
        return re.search(tag_name + " = ['\"]([^'\"]+)['\"]", src).group(1)

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='SimpleScraper',
    version=get_tag('__version__'),
    url='https://github.com/ROZ32/pythonScraper',
    license='MIT License',
    author='Oscar Sanchez',
    tests_require=['pytest'],
    install_requires=['beautifulsoup4','html5lib'],
    cmdclass={'test': PyTest},
    author_email=get_tag('__author__'),
    description='A simple python web scraper',
    long_description=long_description,
    packages=['pythonScraper'],
    include_package_data=True,
    platforms='any',
    test_suite='pythonScraper.test.test_SimpleScraper',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
        ],
    extras_require={
        'testing': ['pytest'],
    }
)