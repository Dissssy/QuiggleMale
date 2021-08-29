# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from setuptools_rust import Binding, RustExtension, Strip
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt","rb") as fh:
    install_requires=[l.strip() for l in fh]

extras_require = {}

setup(
    use_scm_version={"write_to": "__version__.py"},
    name="QuigglePrime",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dissssy/QuiggleMale",

    packages=find_packages(),
    entry_points={},
    install_requires=[],
    setup_requires=["setuptools","setuptools-scm", ],
    extras_require=extras_require,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: Windows",
        "Operating System :: Linux",
    ],
    include_package_data=True,
    zip_safe=False,
)
