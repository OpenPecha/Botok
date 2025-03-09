from botok.tokenizers.stacktokenizer import tokenize_in_stacks


def test_stack_tokenizer():
    """Test the stack tokenizer functionality."""
    # Test with standard Tibetan text
    assert tokenize_in_stacks("ཀཿཐོག་འབྱམ་པའཱི་རོ།") == ["ཀ", "\u0f7f", "ཐོ", "ག", "་", "འ", "བྱ", "མ", "་", "པ", "འཱི", "་", "རོ", "།"]
    
    # Test with special character at the beginning
    assert tokenize_in_stacks("\u0f7fཀཿ") == ["\u0f7f", "ཀ", "\u0f7f"]
    
    # Test with empty string
    assert tokenize_in_stacks("") == []
    
    # Test with single character
    assert tokenize_in_stacks("ཀ") == ["ཀ"]
