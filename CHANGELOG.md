# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

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
