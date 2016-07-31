#!/usr/bin/env python 
from setuptools import setup

setup(
    name="pytest_profile",
    packages = ['pytest_profile'],

    # the following makes a plugin available to pytest
    entry_points = {
        'pytest11': [
            'pytest_profile = pytest_profile',
        ]
    },

    # custom PyPI classifier for pytest plugins
    classifiers=[
        "Framework :: Pytest",
    ],
)
