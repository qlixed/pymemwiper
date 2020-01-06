#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import print_function, absolute_import

import io
import os
import re
from glob import glob
from os.path import join, dirname, relpath, basename, splitext

from setuptools import Extension, setup, find_packages


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8"),
    ) as fh:
        return fh.read()


# Enable code coverage for C code: we can't use CFLAGS=-coverage in tox.ini, since that may mess with compiling
# dependencies (e.g. numpy). Therefore we set SETUPPY_CFLAGS=-coverage in tox.ini and copy it to CFLAGS here (after
# deps have been safely installed).
if "TOXENV" in os.environ and "SETUPPY_CFLAGS" in os.environ:
    os.environ["CFLAGS"] = os.environ["SETUPPY_CFLAGS"]

if "CFLAGS" in os.environ:
    os.environ["CFLAGS"] = " ".join((os.environ["CFLAGS"], "-DMEMWIPER_DEBUG=1"))
else:
    os.environ["CFLAGS"] = "-DMEMWIPER_DEBUG=1"

setup(
    name="memwiper",
    version="0.9.0",
    license="MIT",
    description="Let you overwrite with garbage your inmutable strings easily",
    long_description="%s\n%s"
    % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        ),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Ezequiel Hector Brizuela (qlixed)",
    author_email="qlixed@gmail.com",
    url="https://github.com/qlixed/python-memwiper",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        "Topic :: Utilities",
        "Private :: Do Not Upload",
    ],
    project_urls={
        "Documentation": "https://python-memwiper.readthedocs.io/",
        "Changelog": "https://python-memwiper.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://github.com/qlixed/python-memwiper/issues",
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=["pytest-runner",],
    ext_modules=[
        Extension(
            splitext(relpath(path, "src").replace(os.sep, "."))[0],
            sources=[path],
            include_dirs=[dirname(path)],
        )
        for root, _, _ in os.walk("src")
        for path in glob(join(root, "*.c"))
    ],
)
