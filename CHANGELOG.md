# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

---

## [0.2.0](https://github.com/Esukhia/pybo/releases/tag/v0.2.0) - 20180709
### Added
 * two new attibrutes on the tokens: freq (the word/syllabe frequency) and skrt (test the syllabe composition if it's a sanskrit syllabe or not)
 * mgd trie file (the Monlam Grand Dictionary) and two frequency files (mgd and tc)
 * MGD profile which uses mgd in Trie along with its frequency file

### Changed
 * POS profile uses now the mdg frequency file
 * clear distinction between "OOV" (is in the trie but does not have any POS tag informations) and "non-word" (the syllabe is not part of the Trie)

### Fixed
 * Missing syllabes and punctuations related to the issue #21
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
