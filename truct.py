from pybo import WordTokenizer
from memory_profiler import profile


def get_tok(profile):
    return WordTokenizer(profile)


@profile
def test_tok():
    tsik = get_tok("tsikchen")
    pos = get_tok("POS")
    gmd = get_tok("GMD")


if __name__ == "__main__":
    test_tok()
