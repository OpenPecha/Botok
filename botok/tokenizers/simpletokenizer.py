# coding: utf-8
from .token import Token
from ..chunks.chunks import TokChunks
from ..vars import ChunkMarkers as c
from ..vars import CharMarkers as a
from ..vars import chunk_values, char_values
import unicodedata

class SimpleTokenizer:
    """
    A simple tokenizer that doesn't use a dictionary (just syllabifies).
    Equivalent to the SimpleTokenizer in botok-rs.
    """
    @staticmethod
    def tokenize(text, space_as_punct=False):
        # Normalize Unicode (NFC normalization)
        normalized = unicodedata.normalize('NFC', text)
        
        # Use TokChunks to get syllables and chunks
        tok_chunks = TokChunks(normalized, space_as_punct=space_as_punct)
        tok_chunks.serve_syls_to_trie()
        
        tokens = []
        for syl_idx, chunk in tok_chunks.chunks:
            # chunk is (type, start, len)
            chunk_type, start, length = chunk
            
            token = Token()
            token.text = normalized[start:start+length]
            token.start = start
            token.len = length
            token.chunk_type = chunk_values.get(chunk_type, chunk_type)
            
            if syl_idx is not None:
                # syl_idx is a list of character indices for the syllable
                # we need to store it in syls_idx as expected by Token class
                # The Token class expects indices relative to the token text
                token.syls_idx = [[i - start for i in syl_idx]]
                token.syls_start_end = [{"start": 0, "end": length}]
            
            # Populate char_types as expected by Token
            char_groups = tok_chunks.bs.export_groups(
                start, length, for_substring=True
            )
            token.char_types = [char_values[char_groups[idx]] for idx in sorted(char_groups.keys())]
            
            tokens.append(token)
            
        return tokens
