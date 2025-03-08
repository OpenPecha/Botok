#! /usr/bin/env python
# coding: utf8

from __future__ import print_function

import re
from pathlib import Path

import setuptools
from pkg_resources import parse_version

assert parse_version(setuptools.__version__) >= parse_version("38.6.0")


def get_version(prop, project):
    project = Path(__file__).parent / project / "vars.py"
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
        project.read_text(encoding="utf-8-sig"),
    )
    return result.group(1)


def read(fname):
    p = Path(__file__).parent / fname
    with p.open(encoding="utf-8-sig") as f:
        return f.read()


setuptools.setup(
    name="botok",
    version=get_version("__version__", "botok"),  # edit version in botok/vars.py
    author="OpenPecha development team",
    author_email="openpecha@gmail.com",
    description="Tibetan Word Tokenizer",
    license="Apache2",
    keywords="nlp computational_linguistics tibetan tokenizer token",
    url="https://github.com/OpenPecha/botok",
    packages=setuptools.find_packages(),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    project_urls={
        "Source": "https://github.com/OpenPecha/botok",
        "Tracker": "https://github.com/OpenPecha/botok/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Tibetan",
    ],
    package_data={
        "botok": [
            "resources/*",
            "resources/words_bo/*",
            "resources/entry_data/*",
            "resources/words_non_inflected/*",
            "resources/lemmas/*",
            "resources/rules/*",
            "resources/words_skrt/*",
            "resources/adjustment/*",
        ]
    },
    python_requires=">=3.7",
    tests_require=["pytest>=5.0.0"],
    install_requires=["pyyaml", "requests"],
)
