# pybo

A word tokenizer for Tibetan language. Takes in chunks of text, and returns lists of words. 

## Getting Started 

    pip install pybo

## Goals of pybo

Using pybo, one should be able to:

 1. pre-process any Tibetan string for tokenization
 2. tokenize any pre-processed string into a sequence of word/non-word tokens
 3. apply matchers over the tokenized text (list of Token objects) to modify the segmentation
 4. transform the list of Token objects to and from a spaCy Doc object.  

### 1. Tibetan String Pre-processing

Status: Done.

Strategy:
 - BoString attributes a type to every char in the input string.
 - BoChunk creates chunks of similar chars. (subclass of BoString)
 - PyBoChunk creates meaningful chunks for Tibetan language: syl / (other)bo / punct / non-bo. (subclass of BoChunk)
 - PyBoTextChunks provides cleaned content for syllable chunks (no punct no space). (subclass of PyBoChunk) 

### 2. Tokenization of pre-processed string 

Status: Implemented. Cleanup to be done.

Strategy:

 - SylComponents gives morphologic information about a Tibetan syllable.
 - BoSyl (uses SylComponents):
     - BoSyl.is_affixable(): tells whether a given syllable can be affixed or not
     - BoSyl.get_all_affixed(): for a given syllable, gives all affixed variants. 
        for each variant, gives: 1. the final form, 2. the particle used, 3. True if its non-affixed version ends with འ, False otherwise
 - Trie + Node: Object Oriented Trie implementation
 - PyBoTrie (subclass of Trie, uses BoSyl):
     - builds a trie from a lexicon 
     - adds affixed particle and POS information in the trie
     - allows to dynamically add / deactivate entries in a trie
     - walks an existing trie to find the longest possible match
 - Tokenizer (uses PyBoTrie and Token):
     - input: pre-processed syllables from PyBoTextChunks
     - parses sequences of clean syllables to find the longest word inside the loaded trie
     - builds a word token from a sequence of syllable chunks.
     - builds a Token object from individual chunks (non-bo, punct) and from a word token.
 - SplitAffixed splits Token objects that end with an affixed particle into 1. the token, 2. a token for the affixed particle   

Todo:

 - rename Token object into Token
 - remove tibetaneditor specific attributes and properties + find a way of reimplementing them within tibetaneditor
 - implement SplitAffixed:
     - check in Token.tag if there is an affixed particle
     - use the given particle type to reconstruct the lemma
     - use the given particle length to know where Token.content should be split
     - add a final འ to the lemma of the host Token if needed

### 3. Applying Matchers

Status: Implementation ongoing.

Strategy:

 - Matcher finds sequences of Token objects that match a given input CQL query
 - Splitter takes a Token object and splits it in two.
     - input: the index in Token.content where to split
 - Merger takes two consecutive Token objects to create a merged Token object.
    (the metadata attributes from one token are discarded, the content attributes are concatenated)
 - BoMatcher (uses Matcher and either Splitter or Merger):
     - input: a list of Token object, a matcher, a Splitter / a Merger
     - loops over a list of Token objects (output of Tokenizer)
         - checks whether the sublist[current index: current index + len(matcher)] satisfies Matcher
         - applies either Splitter or Merger if necessary
     - output: the modified list of Token objects

Todo:

 - replace the basic query parser by `third-party/cql.py`
 - move the matching logic from BoMatcher to Matcher
 - implement Splitter
 - implement Merger
 - implement BoMatcher

### 4. To and From spaCy

Status: To do.

Strategy:

 - use the spaCy api to make the conversion

## Licence

The code is provided under [Apache Licence 2.0](LICENSE). Copyright ESUKHIA.
