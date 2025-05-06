#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="pymodoro",
    version="1.0",
    # Modules to import from other scripts:
    packages=find_packages(),
    # Executables
    scripts=["pymodoro"],
)
