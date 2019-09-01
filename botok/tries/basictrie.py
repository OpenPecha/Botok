# coding: utf-8

# inspired from https://gist.github.com/nickstanisha/733c134a0171a00f66d4
# and           https://github.com/eroux/tibetan-phonetics-py


class Node:
    def __init__(self, label=None, leaf=False, data=None):
        if data is None:
            data = {"_": {}}  # the dict in '_' is for user-data
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
        # adding the word
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

        # adding data to the node
        if data:
            assert isinstance(data, dict)
            current_node.data.update(data)

    def walk(self, char, current_node=None):
        # logic of walking the trie adapted to be done outside the trie class (for Tokenize)
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
            return {"exists": exists, "data": current_node.data}
        else:
            return {"exists": exists, "data": current_node.data}

    def add_data(self, word, data):
        """Adds data to words.

        :param word: word to add
        :param data: dict of content to add
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

        # adding data
        if isinstance(data, int):
            current_node.data["form_freq"] = data
            added = True
        else:
            if "entries" not in current_node.data:
                current_node.data["entries"] = []
            added = self.add_meaning(current_node.data["entries"], data)
        return added

    def add_meaning(self, meanings, meaning):
        if meanings:
            for m in meanings:
                if self.is_diff_meaning(meaning, m):
                    meanings.append(meaning)
                    return True
            return False
        else:
            meanings.append(meaning)
            return True

    @staticmethod
    def is_diff_meaning(m1, m2):
        is_diff = False
        for k, v in m1.items():
            if k not in m2 or k in m2 and m2[k] != v:
                is_diff = True
        return is_diff

    def deactivate(self, word, rev=False):
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
