#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jorge Niedbalski R. <jnr@metaklass.org>'


from setuptools import setup, find_packages

dependencies = ["PyYaml"]

setup(
    name="juju-deployerizer",
    version="0.1.5",
    author="Jorge Niedbalski R.",
    include_package_data=True,
    author_email="jnr@metaklass.org",
    description="",
    install_requires=dependencies,
    packages=find_packages(),
    test_suite='nose.collector',
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
    entry_points="""
[console_scripts]
juju-deployerizer = juju_deployerizer.cli:main
"""
)
