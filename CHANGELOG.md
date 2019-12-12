# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.7.3](https://github.com/Esukhia/botok/releases/tag/v0.7.3) - 20191212
### Fixed
 * `botok.__version__` was not available

## [0.7.2](https://github.com/Esukhia/botok/releases/tag/v0.7.2) - 20191212
### Fixed
 * install not working on Windows (encoding not declared in setup.py)

## [0.7.1](https://github.com/Esukhia/botok/releases/tag/v0.7.1) - 20191211
### Added
 * Automated update of existing compiled tries and config files (version included in trie and .yaml, then checked at load time)

## [0.7.0](https://github.com/Esukhia/botok/releases/tag/v0.7.0) - 20191210
### Changed
 * All trie data previously in botok/resources/ is moved to the botok_data repo
 The files are automatically downloaded from botok_data if it is not present, or external profiles can also be used.
 * only the files corresponding to POS profile are kept in botok_data
 * change from word lists to create the trie + entry_data to word lists containing the data (no more duplication of word lists)
 * Token.entries changed to Token.senses
### Added
 * Token.sense added

## [0.6.18](https://github.com/Esukhia/botok/releases/tag/v0.6.18) - 20191121
### Changed
 * yaml format changed to tsv for adjustment rules files. (See syntax [here](https://github.com/Esukhia/botok/blob/master/botok/modifytokens/adjusttokens.py#L11-L24))
 * changed default text field (previously "word", now "text_cleaned") in third_party/pynpl/cql.py

## [0.6.17](https://github.com/Esukhia/botok/releases/tag/v0.6.17) - 20191107
### Fixed
 * fix : when there are custom adjustments, ignore the default adjustments

## [0.6.16](https://github.com/Esukhia/botok/releases/tag/v0.6.16) - 20191107
### Fixed
 * bugfix: custom location for pybo.yaml works
### Added
 * export either all data, or a profile's data (empty, POS, GMD, tsikchen) in expose_data()

## [0.6.15](https://github.com/Esukhia/botok/releases/tag/v0.6.15) - 20191106
### Added
 * add expose_data() to copy at a given location the data used by botok
### Changed
 * remove rdr_2_replace_matchers from botok (into its own repo)

## [0.6.14](https://github.com/Esukhia/botok/releases/tag/v0.6.14) - 20191105
### Added
 * add syllable-mode in token_split
    * expose syllable boundaries from preprocessing into Token objects
    * update boundaries at token splitting and token merging

## [0.6.13](https://github.com/Esukhia/botok/releases/tag/v0.6.13) - 20191101
### Fixed
 * changed the order of entry_data files to: "form / pos / lemma / sense / freq", to have mostly used fields on the left
 * changed "meaning" field in entry_data to "sense"
 * changed entry_data file extension. from .csv to .tsv (content was already tab-delimited)
 * removed the frequency folder in the trie data. it is expected that every line in the entry_data files creates a new sense, in case a single word appears more than once.
### Added
 * Added a lemma in MergeDagdra: the lemma of the host + the dagdra

## [0.6.12](https://github.com/Esukhia/botok/releases/tag/v0.6.12) - 20191007
### Fixed
 * MergeDagdra (in WordTokenizer) does not jump words to merge anymore
 * "lexica" changed to "words" in the resources' folder to improve readability.
 * added missing __version__ attribute in package

## [0.6.11](https://github.com/Esukhia/botok/releases/tag/v0.6.11) - 20191004
### Fixed
 * before a space, ཀ ག ཤ eventually followed by a vowel is now treated as a syllable break
### Added
 * spaces_as_punct optional argument in WordTokenizer.tokenize().
 Dakje Editor required to have spaces and \n in separate tokens instead of having them as transparent chars.

## [0.6.10](https://github.com/Esukhia/botok/releases/tag/v0.6.10) - 20190912
### Added
 * custom path for config files and pickle files

## [0.6.9](https://github.com/Esukhia/botok/releases/tag/v0.6.9) - 20190901
### Added
 * only the tokenizer's codebase is kept in botok repo. everything else is moved to the new pybo repo.

## [0.6.8](https://github.com/Esukhia/pybo/releases/tag/v0.6.8) - 20190826
### Fixed
 * ../ in Path freezing on Mac

## [0.6.7](https://github.com/Esukhia/pybo/releases/tag/v0.6.7) - 20190821
### Added
 * batch regex from file + cli

## [0.6.6](https://github.com/Esukhia/pybo/releases/tag/v0.6.6) - 20190820
### Added
 * RDR rules parser to convert them into pybo's CQL ReplaceMatcher format
 * integrate it in WordTokenizer and Config (same options as for the trie data and profiles)
 * add a CLI option using parse_rdr_rules().

## [0.6.5](https://github.com/Esukhia/pybo/releases/tag/v0.6.5) - 20190816
### Fixed
 * particles not in the list were bugging

## [0.6.4](https://github.com/Esukhia/pybo/releases/tag/v0.6.4) - 20190815
### Added
 * CLI interface for basic tokenization of strings and files

## [0.6.3](https://github.com/Esukhia/pybo/releases/tag/v0.6.3) - 20190814
### Fixed
 * remove print() that was executed at every added word

## [0.6.2](https://github.com/Esukhia/pybo/releases/tag/v0.6.2) - 20190814
### Added
 * implemented sentence and paragraph tokenizers + Text properties
 * meaning field in the entries attribute of Token objects
### Changed
 * reduced the amount of times WordTokenizers were loaded in the test suite (for Travis)
 * improve names for higher consistency
### Fixed
 * a few remaining bugs from previous release

## [0.6.1](https://github.com/Esukhia/pybo/releases/tag/v0.6.1) - 20190813
### Fixed
 * affixed particles were inflected
 * pos, lemma and frequency are brought together: a single inflected form can be two different words, thus different POS and different frequency.
 * various bugs related to the refactoring
### Added
 * support for more than one meaning for every trie entry (inflected form)

A `meanings` attribute is added in the Token objects. They hold as many meanings as found in the trie data.
A default meaning is chosen, then the `pos`, `lemma` and `freq` fields are copied from the `meanings` attribute to the attributes bearing these names.
When only one meaning is available, it is chosen, otherwise, the meaning with the highest amount of attributes is chosen from the following groups, in this order:
meanings that are unaffixed words, meanings that don't have the `affixed` attribute, meanings that are affixed words.

 * adjustments required by the above in the different parts of pybo

## [0.6.0](https://github.com/Esukhia/pybo/releases/tag/v0.6.0) - 20190701
### Changed
 * refactoring the Pipeline class into the Text class. check test_text.py to have an overview of what it does.

## [0.5.1](https://github.com/Esukhia/pybo/releases/tag/v0.5.1) - 20190629
### Added
 * Added a default profile to WordTokenizer so the end user can simply import it and run it without thinking about anything else.

## [0.5.0](https://github.com/Esukhia/pybo/releases/tag/v0.5.0) - 20190627
### Changed
 * Whole refactorisation of pybo's existing features. (Pipeline is not yet refactored)
 * A lot of renaming to clarify things
 * General cleanup of all files and re-organization into folders each containing the files
 * Attribute names of Token objects are changed
### Fixed
 * various bugs, like the how many transparent chars(spaces and tseks) can be inside a syllable
### Added
 * Tests for each file showcasing the expected behaviour (tests for matchers are still the same as before)

## [0.4.3](https://github.com/Esukhia/pybo/releases/tag/v0.4.3) - 20190517
### Fixed
 * bugfix: the yaml warning is fixed
 * bugfix: an infinite loop is fixed
 * bugfix: papomerge is fixed

## [0.4.2](https://github.com/Esukhia/pybo/releases/tag/v0.4.2) - 20190306
### Added
 * BoPipeline now accepts naming custom pipes. a (string, function) is allowed as argument 
   (Warning: not thoroughly tested)
 * dummy pipes are added for preprocessing, processing and formatting.

## [0.4.1](https://github.com/Esukhia/pybo/releases/tag/v0.4.1) - 20190306
### Added
 * BoPipeline is now a class with 4 arguments, one for each pipe. 
   (Warning: not thoroughly tested)

## [0.4.0](https://github.com/Esukhia/pybo/releases/tag/v0.4.0) - 20190305
### Added
 * MergePaPo class. Any token containing པ་/པོ་/བ་/བོ་ in Token.clean_content is by default merged to the previous one
### Changed
 * SplitAffixed was moved from Tokenizer to BoTokenizer, meaning that Tokenizer outputs tokens as they come out from the trie.
   BoTokenizer also hosts LemmatizeTokens.
 * A bit of cleanup

## [0.3.0](https://github.com/Esukhia/pybo/releases/tag/v0.3.0) - 20190201
### Added
 * BoPipeline class. This allows to easily establish a custom pipeline that includes the BoTokenizer
   The tests are limited to the intended functionality. The default pipes should be cleaned and rethought.

## [0.2.21](https://github.com/Esukhia/pybo/releases/tag/v0.2.21) - 20191301
### Fixed
 * CQL matcher didn't match last token

## [0.2.20](https://github.com/Esukhia/pybo/releases/tag/v0.2.20) - 20181221
### Fixed
 * didn't install well on Windows.

## [0.2.19](https://github.com/Esukhia/pybo/releases/tag/v0.2.19) - 20181207
### Fixed
 * files to delete didn't get deleted (wrong variable name)

### Added
 * Deletes all the inflected variants of a given word in the trie instead of just the given (uninflected) variant

## [0.2.18](https://github.com/Esukhia/pybo/releases/tag/v0.2.18) - 20181026
### Fixed
 * bugfix: couldn't attach the content of second chunk of spaces in case two chunks in a row contain only spaces

    While attaching the content of space chunks to the previous chunk, if the previous chunk was a space chunk and its content already attached, the only thing remaining is a bool False as space-holder.
    In this case, if the current chunk is also a space chunk, it couldn't attach to the previous chunk.

    Now goes back to the last valid chunk and attaches content to it.
    

## [0.2.17](https://github.com/Esukhia/pybo/releases/tag/v0.2.17) - 20181026
### Added
 * `deactivate_wordlist()` method to `pybotrie`. This dynamically deactivates lists of words in the trie

## [0.2.16](https://github.com/Esukhia/pybo/releases/tag/v0.2.16) - 20181023
### Added
 * new affix combinations (see [#25](https://github.com/Esukhia/pybo/issues/25))
 * externalized trie profiles in config files
 * added `\t` to the space list in BoSyl (sometimes used instead of a space)
 * added tibetan-verbs-database to MGD trie profile
 * added frequency info to the trie

### Changed
 * improve and simplify setup.py
 * improve `Token.__repr__()`
 * if there is a space after a shed, put the space in the punctuation token instead of the next syllable 
    and merge into 1 token only the བཞི་ཤད་
    
    ex:
    
    `["།", " བཀྲ་ཤིས་"]` -> `["། ", "བཀྲ་ཤིས་"]` and  `["།། ", "།།"]` -> `["།། །།"]`

    Nota: both "༎" (Tibetan Mark Nyis Shad `U+0F0E`) and "།།" (Tibetan Mark Shad x 2 `U+0F0DU+0F0D`) are supported
 * mgd.txt and sanskrit.txt have been cleaned up and updated

### Fixed
 * when tokenizing without splitting the affixed particles, the unaffixed_word attribute added a འ to words not needing it. 
   (རྒྱ་མཚོར་ gave རྒྱ་མཚོའ་)
 * missing tseks are now detected after char types 'numbers', 'other' and 'symbols'
 * `long_skrt_vowel` (Tibetan Sign Rnam Bcad `U+0F7F`) is treated as syllable content. It triggers a syllable change, 
    as the tsek already does. (a tsek is not added in the presence of a `long_skrt_vowel`)
 * added mechanism to generate tokens of type `numbers` (previously considered symbols)

---

## [0.2.2](https://github.com/Esukhia/pybo/releases/tag/v0.2.2) - 20180711
### Added
 * two new tests in order to check the frequency of a token and if a syllable is sanskrit

### Fixed
 * [The resources for the frequency is not in the package #23](https://github.com/Esukhia/pybo/issues/23)

---

## [0.2.1](https://github.com/Esukhia/pybo/releases/tag/v0.2.1) - 20180711
### Added
 * two new attibrutes on the tokens: `char_types` (type of characters in a syllable) and `type` (type of the token)

### Changed
 * token.lenght is now renamed to **token.len**
 * `char types` (print-out attribute of a token) is now renamed to `char_types`
 * `start in input` (print-out attribute of a token) is now renamed to `start`
 * `syl chars in conten` (print-out attribute of a token) is now renamed to `syls`
 * `POS` (print-out attribute of a token) is now renamed to `pos`

### Fixed
 * [symbol considered as token content #19](https://github.com/Esukhia/pybo/issues/19)
 * [suggestion for token conventions #12](https://github.com/Esukhia/pybo/issues/12)

---

## [0.2.0](https://github.com/Esukhia/pybo/releases/tag/v0.2.0) - 20180709
### Added
 * two new attibrutes on the tokens: `freq` (the word/syllable frequency) and `skrt` (test the syllable composition if it's a sanskrit syllable or not)
 * mgd (the Monlam Grand Dictionary) and two frequency files (mgd and tc) - See the [README file](https://github.com/Esukhia/pybo/blob/master/pybo/resources/README.md) in ressource for more informations
 * MGD profile which uses mgd in trie along with its frequency file

### Changed
 * POS profile now uses the mdg frequency file
 * clear distinction between "OOV" (is in the trie but does not have any POS tag informations) and "non-word" (the syllable is not part of the trie)

### Fixed
 * [Missing syllable and punctuations issue #21](https://github.com/Esukhia/pybo/issues/21)
 * invalid PATH in some test files

---

## [0.1.4](https://github.com/Esukhia/pybo/releases/tag/v0.1.4) - 20180425
### Added
 * Changelog

### Changed
 * improve setup.py readability

### Fixed
 * missing argument to add POS tags in POS profile

---

## [0.1.3](https://github.com/Esukhia/pybo/releases/tag/v0.1.3) - 20180425
### Added
 * initial release
