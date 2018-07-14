import csv

# Simple decorated Trie with helper functions

## inspired from https://gist.github.com/nickstanisha/733c134a0171a00f66d4

class Node:
    def __init__(self, label=None, data=None, canbefinal=True):
        self.label = label
        self.data = data
        self.canbefinal = canbefinal
        self.children = {}
    
    def addChild(self, key, data=None, canbefinal=True):
        if not isinstance(key, Node):
            self.children[key] = Node(key, data, canbefinal)
        else:
            self.children[key.label] = key
    
    def __getitem__(self, key):
        return self.children[key]

class Trie:
    def __init__(self):
        self.head = Node()
    
    def __getitem__(self, key):
        return self.head.children[key]
    
    def add(self, word, data=True, canbefinal=True):
        current_node = self.head
        for c in word:
            if c not in current_node.children:
                current_node.addChild(c)
            current_node = current_node.children[c]
        current_node.data = data
        current_node.canbefinal = canbefinal
    
    def get_longest_match_with_data(self, word, bindex=0, eindex=-1, ignored_chars=None):
        current_node = self.head
        if eindex == -1:
            eindex = len(word)
        latest_match_node = None
        if current_node.data:
            latest_match_node = current_node
        latest_match_i = bindex
        for i in range(bindex, eindex):
            letter = word[i]
            if ignored_chars and letter in ignored_chars:
                if latest_match_i == i:
                    # if we just matched, consider that the following ignored chars
                    # are also part of the match
                    latest_match_i = i+1
                continue
            if letter in current_node.children:
                current_node = current_node.children[letter]
                #print("i: "+str(i)+", eindex: "+str(eindex))
                if current_node.data and (i+1 < eindex or current_node.canbefinal):
                    latest_match_node = current_node
                    latest_match_i = i+1
            else:
                break
        if latest_match_node == None:
            return None
        return {"i": latest_match_i, "d": latest_match_node.data}

    def get_data(self, word, bindex=0, eindex=-1, ignored_chars=None):
        current_node = self.head
        if eindex == -1:
            eindex = len(word)
        for i in range(bindex, eindex):
            letter = word[i]
            if ignored_chars and letter in ignored_chars:
                continue
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                return None
        return current_node.data

    def _walk_all_data_rec(self, iterator, node, word, prefix):
        """ Recursive function walking the tree """
        # If we're still in the prefix:
        if len(prefix) > 0:
            letter = prefix[0]
            if letter in node.children:
                child_node = top_node.children[letter]
                self._walk_all_data_rec(iterator, child_node, word+letter, prefix[1:])
            return
        if node.data:
            iterator(word, node.data)
        for letter, child_node in node.children.items():
            self._walk_all_data_rec(iterator, child_node, word+letter, prefix)

    def walk_all_data(self, iterator, prefix=''):
        """ Iterates over all the data of a trie """
        self._walk_all_data_rec(iterator, self.head, '', prefix)
        

Cx_to_vow = {'a': '', 'b': '', 'c': '', 'i': 'ི', 'u': 'ུ', 'e': 'ེ', 'o': 'ོ'}
Cx_affix_list = ['', 'འི', 'འིའོ', 'འོ', 'འང', 'འམ', 'ར', 'ས']
Cx_affix_list_a = ['འ', 'འི', 'འིའོ', 'འོ', 'འང', 'འམ', 'ར', 'ས']
Cx_suffix_list = ['འ', 'འི', 'འིའོ', 'འོ', 'འང', 'འམ', 'ར', 'ས', 'ག', 'གས', 'ང', 'ངས', 'ད', 'ན', 'བ', 'བས', 'མ', 'མས', 'ལ']

def add_association_in_trie(unicodeTib, phonStr, trie, phonType, endsTrie=None):
    if len(unicodeTib) > 2 and unicodeTib[-3] == '/' and unicodeTib[-2] == 'C':
        letter = unicodeTib[-1:]
        vow = Cx_to_vow[letter]
        # convention:
        # - b is for when all suffixes are possible, including འ, but an absence of suffix is not
        # - c is for when all affixes are possible, but in the absence of affix, འ is mandatory
        suffix_list = Cx_affix_list
        if letter == 'b':
            suffix_list = Cx_suffix_list
        if letter == 'c':
            suffix_list = Cx_affix_list_a
        for affix in suffix_list:
            phonVowAffix = endsTrie.get_data(vow+affix)
            #print("add in trie: "+unicodeTib[0:-3]+affix+" -> "+phonStr+phonVowAffix)
            add_association_in_trie(unicodeTib[0:-3]+affix, phonStr+phonVowAffix, trie, phonType)
        return
    if unicodeTib.startswith('2:'):
        trie.add(unicodeTib[2:], '2:'+phonStr)
    if unicodeTib.endswith('*'):
        trie.add(unicodeTib[0:-1], phonStr, False)
    else:
        trie.add(unicodeTib, phonStr)

def get_trie_from_file(filename, phonType="roots", columnIndex = 1, endsTrie=None):
    trie = Trie()
    with open(filename, newline='', encoding="utf8") as csvfile:
        freader = csv.reader(csvfile)
        for row in freader:
            if row[0].startswith('#'):
                continue
            if len(row) > columnIndex:
                add_association_in_trie(row[0], row[columnIndex], trie, phonType, endsTrie)
            elif phonType != "exceptions":
                add_association_in_trie(row[0], '', trie, phonType, endsTrie)
    return trie

if __name__ == '__main__':
    """ Example use """
    trie = Trie()
    trie.add("test", "test_data")
    trie.add("t", "t_data")
    print(trie.get_longest_match_with_data("test"))
    print(trie.get_data("test"))
    print(trie.get_longest_match_with_data("tes"))
    trie.add("te", "te_data", False)
    print(trie.get_longest_match_with_data("tes"))
    print(trie.get_longest_match_with_data("te"))
    def iteratortest(word, data):
        print("data for \""+word+"\": "+data)
    trie.walk_all_data(iteratortest)
