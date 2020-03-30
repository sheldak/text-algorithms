class Trie:
    def __init__(self):
        self._root = Node()
        self._suffixes = 0

    def add_suffix(self, suffix):
        curr_letter = 0
        curr_node = self.root
        while curr_letter < len(suffix):
            if suffix[curr_letter] in curr_node.children:
                curr_node = curr_node.children[suffix[curr_letter]]
                curr_letter += 1
            else:
                break

        for i in range(curr_letter, len(suffix)):
            curr_node.add_child(suffix[i])
            curr_node = curr_node.children[suffix[i]]

        self._suffixes += 1

    def find(self, word):
        curr_node = self.root
        for curr_letter in range(len(word)):
            if word[curr_letter] in curr_node.children:
                curr_node = curr_node.children[word[curr_letter]]
            else:
                return False

        return True

    @property
    def root(self):
        return self._root

    @property
    def suffixes(self):
        return self._suffixes


class Node:
    def __init__(self):
        self._children = {}

    def add_child(self, letter):
        self._children[letter] = Node()

    @property
    def children(self):
        return self._children


def make_suffix_trie(word):
    trie = Trie()
    for i in range(len(word)):
        trie.add_suffix(word[i:])

    return trie
