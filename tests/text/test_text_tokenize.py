from botok.text.tokenize import space_tok, word_tok, sentence_tok, paragraph_tok
from botok.config import Config


def test_text_space_tokenizer():
    """Test the space tokenizer functionality."""
    text = "ཀཿ ཐོག་ འབྱམ་ པའཱི་ རོ།"
    tokens = space_tok(text)
    assert len(tokens) == 5
    assert tokens[0] == "ཀཿ"
    assert tokens[1] == "ཐོག་"


def test_text_word_tokenizer():
    """Test the word tokenizer functionality."""
    text = "ཀཿཐོག་འབྱམ་པའཱི་རོ།"
    tokens = word_tok(text)
    assert len(tokens) > 0
    assert hasattr(tokens[0], "text")


def test_text_sentence_tokenizer():
    """Test the sentence tokenizer functionality."""
    text = "ཀཿཐོག་འབྱམ་པའཱི་རོ། འདི་ནི་ཚིག་གྲུབ་གཉིས་པ་ཡིན།"
    sentences = sentence_tok(text)
    # It should have at least one sentence with tokens
    assert len(sentences) > 0
    # The expected output format is a dictionary with sentence data
    assert isinstance(sentences[0], dict)
    assert 'tokens' in sentences[0]
    assert isinstance(sentences[0]['tokens'], list)
    assert len(sentences[0]['tokens']) > 0


def test_text_paragraph_tokenizer():
    """Test the paragraph tokenizer functionality."""
    text = "ཀཿཐོག་འབྱམ་པའཱི་རོ།\n\nའདི་ནི་དུམ་བུ་གཉིས་པ་ཡིན།"
    paragraphs = paragraph_tok(text)
    # It should have at least one paragraph with tokens
    assert len(paragraphs) > 0
    assert isinstance(paragraphs[0], tuple)
    assert len(paragraphs[0]) == 2
    # The first element is the paragraph index
    assert isinstance(paragraphs[0][0], int)
    # The second element is the list of tokens
    assert isinstance(paragraphs[0][1], list)


def test_text_tokenizers_with_config():
    """Test tokenizers with custom configuration."""
    config = Config()
    text = "ཀཿཐོག་འབྱམ་པའཱི་རོ།"
    
    # Test word tokenizer with config
    tokens = word_tok(text, config=config)
    assert len(tokens) > 0
    
    # Test sentence tokenizer with config
    sentences = sentence_tok(text, config=config)
    assert len(sentences) > 0
    
    # Test paragraph tokenizer with config
    paragraphs = paragraph_tok(text, config=config)
    assert len(paragraphs) > 0
