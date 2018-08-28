# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import pymtst.PkgInfo as PkgInfo

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name=PkgInfo.package,
    version=PkgInfo.version,
    description=PkgInfo.short_description,
    long_description=readme,
    long_description_content_type="text/markdown",
    author='hrchu',
    author_email='petertc.chu@gmail.com',
    url=PkgInfo.url,
    license=PkgInfo.license,
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Archiving",
        "Topic :: System :: Hardware",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ),
)
