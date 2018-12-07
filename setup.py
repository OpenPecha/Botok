#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import os
import setuptools
from pkg_resources import parse_version

assert(parse_version(setuptools.__version__) >= parse_version("38.6.0"))


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="pybo",
    version="0.2.19",  # also edit version in pybo/__init__.py
    author="Esukhia development team",
    author_email="esukhiadev@gmail.com",
    description="Python utils for processing Tibetan",
    license="Apache2",
    keywords="nlp computational_linguistics search ngrams language_models linguistics toolkit tibetan",
    url="https://github.com/Esukhia/pybo",
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    project_urls={
        'Source': 'https://github.com/Esukhia/pybo',
        'Tracker': 'https://github.com/Esukhia/pybo/issues',
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Tibetan"
    ],
    package_data={'pybo': ['resources/*', 'resources/trie/*', 'resources/frequency/*', 'resources/lemmas/*', 'resources/rules/*', 'resources/sanskrit/*']},
    python_requires='>=3.4',
    # setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=[
        'pyyaml',
    ],
)
