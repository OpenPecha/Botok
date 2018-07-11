#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import os
import sys
from setuptools import setup, find_packages
import pypandoc

def read(fname):
    rst = pypandoc.convert_file(os.path.join(os.path.dirname(__file__), fname), 'rst', format='md')
    return rst


setup(
    name="pybo",
    version="0.2.2",  # also edit version in pybo/__init__.py
    author="Esukhia development team",
    author_email="esukhiadev@gmail.com",
    description="Python utils for processing Tibetan",
    license="Apache2",
    keywords="nlp computational_linguistics search ngrams language_models linguistics toolkit tibetan",
    url="https://github.com/Esukhia/pybo",
    packages=find_packages(),
    long_description=read('README.md'),
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
    package_data={'pybo': ['resources/*', 'resources/trie/*', 'resources/lemmas/*', 'resources/rules/*', 'resources/frequency/*']},
    python_requires='>=3',
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=[
        'pyyaml'
    ],
)
