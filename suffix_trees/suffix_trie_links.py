from queue import LifoQueue as Stack


class Trie:
    def __init__(self):
        self._root = Node(None, "", 0)

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


class Node:
    def __init__(self, parent, par_letter, depth):
        self._children = {}

        self._parent = parent
        self._parent_letter = par_letter

        self._link = None

        self._depth = depth

    def add_child(self, letter):
        self._children[letter] = Node(self, letter, self.depth+1)

    def print(self):
        print(self._children)
        for child in self._children.values():
            child.print()

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @property
    def parent_letter(self):
        return self._parent_letter

    @property
    def link(self):
        return self._link

    @property
    def depth(self):
        return self._depth

    @link.setter
    def link(self, link):
        self._link = link


def up_link_down(sibling):
    letters = Stack()
    while sibling and not sibling.link:
        letters.put(sibling.parent_letter)
        sibling = sibling.parent

    if not sibling:
        return None, None

    node = sibling.link
    while not letters.empty():
        curr_letter = letters.get()
        if curr_letter in node.children:
            node = node.children[curr_letter]
            sibling = sibling.children[curr_letter]
            sibling.link = node
        else:
            break

    return node, sibling


def graft(node, text, sibling=None):
    for current_letter in text:
        node.add_child(current_letter)
        node = node.children[current_letter]

        if sibling:
            sibling = sibling.children[current_letter]
            sibling.link = node

    return node


def make_suffix_trie(word):
    trie = Trie()
    leaf = graft(trie.root, word)
    trie.root.children[word[0]].link = trie.root
    for i in range(1, len(word)):
        head, sibling = up_link_down(leaf)
        if not head:
            sibling = trie.root.children[word[i-1]]
            sibling.link = trie.root
            head, sibling = up_link_down(leaf)

        leaf = graft(head, word[i+head.depth:], sibling)

    return trie
