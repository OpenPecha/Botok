from botok.tokenizers.stacktokenizer import tokenize_in_stacks


def test_stack_tokenizer():
    assert tokenize_in_stacks("\u0f40\u0f7f\u0f50\u0f7c\u0f42\u0f0b\u0f60\u0f56\u0fb1\u0f58\u0f0b\u0f54\u0f60\u0f71\u0f72\u0f0b\u0f62\u0f7c\u0f0d") == [
        "\u0f40", "\u0f7f", "\u0f50\u0f7c", "\u0f42", "\u0f0b", "\u0f60", "\u0f56\u0fb1",
        "\u0f58", "\u0f0b", "\u0f54", "\u0f60\u0f71\u0f72", "\u0f0b", "\u0f62\u0f7c", "\u0f0d",
    ]
    assert tokenize_in_stacks("\u0f7f\u0f40\u0f7f") == ["\u0f7f", "\u0f40", "\u0f7f"]
    assert tokenize_in_stacks("") == []
    assert tokenize_in_stacks("\u0f40") == ["\u0f40"]


def test_tsa_phru_stays_with_preceding_base():
    assert tokenize_in_stacks("\u0f62\u0f39\u0f72") == ["\u0f62\u0f39\u0f72"]
    assert tokenize_in_stacks("\u0f66\u0fa1\u0f39\u0f74\u0f72") == ["\u0f66\u0fa1\u0f39\u0f74\u0f72"]
    assert tokenize_in_stacks("\u0f56\u0f66\u0fa1\u0f39\u0f74\u0f72\u0f56\u0f51") == [
        "\u0f56", "\u0f66\u0fa1\u0f39\u0f74\u0f72", "\u0f56", "\u0f51",
    ]
    assert tokenize_in_stacks("\u0f55\u0fb1\u0f39\u0f63\u0f7c\u0f51") == [
        "\u0f55\u0fb1\u0f39", "\u0f63\u0f7c", "\u0f51",
    ]
    assert tokenize_in_stacks("\u0f60\u0f41\u0fb2\u0f39\u0f74\u0f7c\u0f51") == [
        "\u0f60", "\u0f41\u0fb2\u0f39\u0f74\u0f7c", "\u0f51",
    ]
    assert tokenize_in_stacks("\u0f66\u0fa1\u0fb2\u0f7c\u0f44\u0f39\u0f7c\u0f51") == [
        "\u0f66\u0fa1\u0fb2\u0f7c", "\u0f44\u0f39\u0f7c", "\u0f51",
    ]
    assert tokenize_in_stacks("\u0f40\u0f74\u0f53\u0f9f\u0f39\u0f74\u0f7e") == [
        "\u0f40\u0f74", "\u0f53\u0f9f\u0f39\u0f74\u0f7e",
    ]


def test_other_stack_marks_stay_with_preceding_base():
    assert tokenize_in_stacks("\u0f40\u0fc6") == ["\u0f40\u0fc6"]
    assert tokenize_in_stacks("\u0f40\u0f3e\u0f72") == ["\u0f40\u0f3e\u0f72"]
    assert tokenize_in_stacks("\u0f40\u0f3f\u0f72") == ["\u0f40\u0f3f\u0f72"]


def test_leading_continuation_marks_are_kept():
    assert tokenize_in_stacks("\u0f72\u0f40") == ["\u0f72", "\u0f40"]
    assert tokenize_in_stacks("\u0f39\u0f72") == ["\u0f39\u0f72"]
