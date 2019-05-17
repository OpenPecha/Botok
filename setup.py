#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

from pathlib import Path
import setuptools
from pkg_resources import parse_version

assert(parse_version(setuptools.__version__) >= parse_version("38.6.0"))


def read(fname):
    p = Path(__file__).parent / fname
    with p.open(encoding='utf-8') as f:
        return f.read()


setuptools.setup(
    name="pybo",
    version="0.4.3",  # also edit version in pybo/__init__.py
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
    python_requires='>=3.6',
    # setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=[
        'pyyaml',
    ],
)
