# coding: utf-8

# inspired from https://gist.github.com/nickstanisha/733c134a0171a00f66d4
# and           https://github.com/eroux/tibetan-phonetics-py


class Node:
    def __init__(self, label=None, leaf=False, data=None):
        self.label = label
        self.leaf = leaf
        self.data = data
        self.children = dict()

    def add_child(self, key, leaf=False):
        if not isinstance(key, Node):
            self.children[key] = Node(key, leaf)
        else:
            self.children[key.leaf] = key

    def can_walk(self):
        return self.children != dict()

    def is_match(self):
        return self.leaf

    def __getitem__(self, key):
        return self.children[key]


class BasicTrie:
    def __init__(self):
        self.head = Node()

    def __getitem__(self, key):
        return self.head.children[key]

    def add(self, word, data=None):
        current_node = self.head
        word_finished = True

        i = 0
        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_finished = False
                break

        if not word_finished:
            while i < len(word):
                current_node.add_child(word[i])
                current_node = current_node.children[word[i]]
                i += 1

        current_node.leaf = True
        if data:
            if current_node.data is None:
                current_node.data = dict()
            current_node.data.update(data)

    def walk(self, char, current_node=None):
        # used in Tokenize
        if not current_node:
            current_node = self.head

        if char in current_node.children:
            next_node = current_node[char]
        else:
            next_node = None

        return next_node

    def has_word(self, word):
        if not word:
            raise ValueError('"word" must be non-null string')

        # parse the word
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break
        else:
            # reached a word like 't', not a full word in our dictionary
            if exists and not current_node.leaf:
                exists = False

        if exists:
            return {'exists': exists, 'data': current_node.data}
        else:
            return {'exists': exists, 'data': current_node.data}

    def add_data_to_word(self, word, data, overwrite=True):
        """Adds data to words.

        :param word: word to add
        :param data: dict of content to add
        :param overwrite: write over existing content
        :return: True if any content added, False otherwise
        """
        if not word:
            raise ValueError('"word" must be non-null string')

        # parse word
        current_node = self.head
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                return False

        # not a complete word
        if not current_node.leaf:
            return False

        # adding data if the data is absent or if overwrite == True
        added = False
        for k, v in data.items():
            if k not in current_node.data:
                current_node.data[k] = v
                added = True
            else:
                if overwrite:
                    current_node.data[k] = v
                    added = True
        return added

    def deactivate_word(self, word, rev=False):
        """Makes word not findable (words are found only when the leaf value is True)

        :param word: word to deactivate
        :param rev: reverse the deactivation
        :return True if the word exists, False otherwise
        """
        current_node = self.head
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                return False
        if isinstance(current_node.data, dict):
            if not rev:
                current_node.leaf = False
            else:
                current_node.leaf = True
            return True
        else:
            return False


if __name__ == '__main__':
    """Example use """
    trie = BasicTrie()
    words = 'hello goo good goodbye help gerald gold tea ted team to too tom stan standard money'
    for n, w in enumerate(words.split()):
        trie.add(w, {'count': n})
    trie.add_data_to_word('goodbye', {'count': 150, 'test': [1, 2, 3]}, overwrite=False)
    trie.deactivate_word('goodbye')
    print("'goodbye':", trie.has_word('goodbye'))
    trie.deactivate_word('goodbye', rev=True)
    print("'goodbye':", trie.has_word('goodbye'))
