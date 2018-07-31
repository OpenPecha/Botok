#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import os
from setuptools import setup, find_packages


def read(fname):
    abs_path = os.path.join(os.path.dirname(__file__), fname)
    rst_path = abs_path.replace('.md', '.rst')

    # 1. installing from the package downloaded from pypi
    # note: only .rst finds its way into the sdist package
    if os.path.exists(rst_path):
        rst = open(rst_path, encoding='utf-8').read()

    else:
        # 2. building the dist to upload to pypi.
        # IMPORTANT: ensure to always have pypandoc installed when preparing a new release.
        # Otherwise, the project page on pypi won't be correct
        try:
            import pypandoc
            rst = pypandoc.convert_file(abs_path, 'rst', format='md')
            # writing parsed content to the .rst file that will be included in the sdist
            # note: the .rst file is in .gitignore, to ensure the repo remains clean
            with open(rst_path, 'w') as f:
                f.write(rst)

        # 3. building locally from the repo.
        # it is assumed we are not uploading to pypi, so having pypandoc is not enforced.
        except (IOError, ImportError):
            rst = open(abs_path, encoding='utf-8').read()

    return rst


setup(
    name="pybo",
    version="0.2.2.1",  # also edit version in pybo/__init__.py
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
    package_data={'pybo': ['resources/*', 'resources/trie/*', 'resources/frequency/*', 'resources/lemmas/*', 'resources/rules/*', 'resources/sanskrit/*']},
    python_requires='>=3',
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=[
        # 'pyyaml',
    ],
)
