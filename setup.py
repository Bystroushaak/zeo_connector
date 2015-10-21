#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup, find_packages
from docs import getVersion


# Variables ===================================================================
changelog = open('CHANGELOG.rst').read()
long_description = "\n\n".join([
    open('README.rst').read(),
    changelog
])


# Actual setup definition =====================================================
setup(
    name='zeo_connector',
    version=getVersion(changelog),
    description="Wrappers, which make working with ZEO little bit nicer.",
    long_description=long_description,
    url='https://github.com/Bystroushaak/zeo_connector',

    author='Bystroushaak',
    author_email='bystrousak@kitakitsune.org',

    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",

        "License :: OSI Approved :: MIT License",
    ],
    license='MIT',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    scripts=[
        # 'bin/edeposit_storage_runzeo.sh',
    ],

    zip_safe=False,
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),

    test_suite='py.test',
    tests_require=["pytest"],
    extras_require={
        "test": [
            "pytest",
        ],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ]
    },
)
