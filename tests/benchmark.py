import urllib.request

import pytest

from botok import WordTokenizer


@pytest.fixture(scope="module")
def testcases():
    file_url = "https://raw.githubusercontent.com/OpenPecha/P000001/master/P000001.opf/base/v001.txt"
    response = urllib.request.urlopen(file_url)
    large_size = response.read().decode("utf-8")
    medium_size = large_size[: len(large_size) // 3]
    small_size = medium_size[: len(medium_size) // 5]
    return large_size, medium_size, small_size


@pytest.fixture(scope="module")
def wt():
    return WordTokenizer()


def test_non_parallized_tok_small(benchmark, wt, testcases):
    _, _, small = testcases

    @benchmark
    def tok():
        wt.tokenize(small)


def test_parallized_tok_small(benchmark, wt, testcases):
    _, _, small = testcases

    @benchmark
    def tok():
        wt.tokenize(small, parallelize=True)


def test_non_parallized_tok_medium(benchmark, wt, testcases):
    _, medium, _ = testcases

    @benchmark
    def tok():
        wt.tokenize(medium)


def test_parallized_tok_medium(benchmark, wt, testcases):
    _, medium, _ = testcases

    @benchmark
    def tok():
        wt.tokenize(medium, parallelize=True)


def test_non_parallized_tok_large(benchmark, wt, testcases):
    large, _, _ = testcases

    @benchmark
    def tok():
        wt.tokenize(large)


def test_parallized_tok_large(benchmark, wt, testcases):
    large, _, _ = testcases

    @benchmark
    def tok():
        wt.tokenize(large, parallelize=True)
