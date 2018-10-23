# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).


## [0.2.16](https://github.com/Esukhia/pybo/releases/tag/v0.2.16) - 20181023
### Added
 * new affix combinations (see [#25](https://github.com/Esukhia/pybo/issues/25))

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
