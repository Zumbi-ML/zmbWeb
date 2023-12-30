#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import find_packages, setup

with open("README.md") as f:
    README = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="zumbi_web",
    version="0.0.1",
    description="The Zumbi Web Site and Apps",
    long_description=app.run(),
    author="Zumbi Intel Team",
    author_email="silva.o.jefferson@gmail.com",
    url="https://github.com/zumbi-ML",
    license=license,
    packages=find_packages(),
    test_suite="zumbi_web",
    tests_require="tests",
)
