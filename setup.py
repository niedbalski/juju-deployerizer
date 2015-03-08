#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jorge Niedbalski R. <jnr@metaklass.org>'

import os
from setuptools import setup, find_packages

dependencies = ["PyYaml"]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="juju-deployerizer",
    version="0.0.1",
    author="Jorge Niedbalski R.",
    include_package_data=True,
    author_email="jnr@metaklass.org",
    description="",
    install_requires=dependencies,
    packages=find_packages(),
    test_suite='nose.collector',
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
    entry_points="""
[console_scripts]
juju-deployerizer = juju_deployerizer.cli:main
"""
)
