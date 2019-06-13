# coding: utf-8

# inspired from https://gist.github.com/nickstanisha/733c134a0171a00f66d4
# and           https://github.com/eroux/tibetan-phonetics-py


class Node:
    def __init__(self, label=None, leaf=False, data=None, freq=None, skrt=None):
        self.label = label
        self.leaf = leaf
        self.data = data
        self.freq = freq
        self.skrt = skrt
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

    def add(self, word, data=None, freq=None, skrt=None):
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
            current_node.data = data
        if freq:
            current_node.freq = freq
        if skrt:
            current_node.skrt = skrt

    def walk(self, char, current_node=None):
        if not current_node:
            current_node = self.head

        if char in current_node.children:
            next_node = current_node[char]
        else:
            next_node = None

        return next_node

    def has_word(self, word):
        if word == '':
            return False
        elif not word:
            raise ValueError('Trie.has_word requires a not-Null string')

        # Start at the top
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break

        # Still need to check if we just reached a word like 't'
        # that isn't actually a full word in our dictionary
        if exists:
            if not current_node.leaf:
                exists = False
        if exists:
            return {'exists': exists, 'data': current_node.data}
        else:
            return {'exists': exists}

    def add_data_to_word(self, word, data, ins, overwrite=False):
        """ Adds data to a word, returns True if the data was added, False otherwise """
        if not word or word == '':
            return False

        current_node = self.head
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                return False

        if not current_node.leaf:
            return False

        to_data = True if ins == "data" else False
        if (to_data and current_node.data) or \
                (to_data == False and current_node.freq):
            if overwrite:
                if to_data:
                    current_node.data = data
                else:
                    current_node.freq = int(data)
                return True
            else:
                return False
        else:
            if to_data:
                current_node.data = data
            else:
                current_node.freq = int(data)
            return True

    def deactivate_word(self, word):
        """
        make the word not findable.

        :return True if the word exists, False otherwise
        """
        current_node = self.head
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                return False
        current_node.leaf = False
        current_node.data = None
        current_node.freq = None
        return True


if __name__ == '__main__':
    """ Example use """
    trie = BasicTrie()
    words = 'hello goo good goodbye help gerald gold tea ted team to too tom stan standard money'
    for w in words.split():
        trie.add(w)
    print("'goodbye':", trie.has_word('goodbye'))
