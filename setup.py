import os
import sys
import re
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


VERSION = ''
with open('nylas/_client_sdk_version.py', 'r') as fd:
    VERSION = re.search(r'^__VERSION__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

RUN_DEPENDENCIES = [
    "requests>=2.4.2",
    "six>=1.4.1",
    "bumpversion>=0.5.0",
    "pyOpenSSL",  # needed for SNI support, required by api.nylas.com
    "ndg-httpsclient",
    "pyasn1",
    "urlobject",
]
TEST_DEPENDENCIES = [
    # These versions are the latest that still have python 2 support
    'astroid==1.6.5',
    'pylint==1.9.3',
    "pytest",
    "pytest-cov",
    "pytest-pylint",
    "responses==0.6.1",
]


class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to pytest"),
        ('lint', None, "Enable linting with pylint"),
    ]

    boolean_options = ['lint']

    def initialize_options(self):
        TestCommand.initialize_options(self)
        # pylint: disable=attribute-defined-outside-init
        self.pytest_args = ['--cov', '--junitxml', './tests/output', 'tests/']
        self.lint = False

    def finalize_options(self):
        TestCommand.finalize_options(self)
        # pylint: disable=attribute-defined-outside-init
        self.test_args = []
        self.test_suite = True
        if self.lint:
            self.pytest_args.append("--pylint")

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def main():
    # A few handy release helpers.
    if len(sys.argv) > 1:
        if sys.argv[1] == 'publish':
            os.system('git push --follow-tags && python setup.py sdist upload')
            sys.exit()
        elif sys.argv[1] == 'release':
            if len(sys.argv) < 3:
                type_ = 'patch'
            else:
                type_ = sys.argv[2]
            os.system('bumpversion --current-version {} {}'
                      .format(VERSION, type_))
            sys.exit()

    setup(
        name="nylas",
        version=VERSION,
        packages=find_packages(),
        install_requires=RUN_DEPENDENCIES,
        dependency_links=[],
        tests_require=TEST_DEPENDENCIES,
        extras_require={'test': TEST_DEPENDENCIES},
        cmdclass={'test': PyTest},
        author="Nylas Team",
        author_email="support@nylas.com",
        description='Python bindings for Nylas, the next-generation email platform.',
        license="MIT",
        keywords="inbox app appserver email nylas contacts calendar",
        url='https://github.com/nylas/nylas-python',
        long_description_content_type='text/markdown',
        long_description='''
# Nylas REST API Python bindings 
[![Build Status](https://travis-ci.org/nylas/nylas-python.svg?branch=master)](https://travis-ci.org/nylas/nylas-python) 
[![Code Coverage](https://codecov.io/gh/nylas/nylas-python/branch/master/graph/badge.svg)](https://codecov.io/gh/nylas/nylas-python)

Python bindings for the Nylas REST API. https://www.nylas.com/docs

The Nylas APIs power applications with email, calendar, and contacts CRUD and bi-directional sync from any inbox in the world.

Nylas is compatible with 100% of email service providers, so you only have to integrate once.
No more headaches building unique integrations against archaic and outdated IMAP and SMTP protocols.''',

    )


if __name__ == '__main__':
    sys.exit(main())
