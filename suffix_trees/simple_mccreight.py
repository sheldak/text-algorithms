class Tree:
    """Structure containing suffix tree"""
    def __init__(self, word):
        self._root = Node()
        self._word = word

    def add_suffix(self, suffix):
        curr_letter = 0
        curr_node = self.root
        while curr_letter < len(suffix) and suffix[curr_letter] in curr_node.children:  # slow find
            curr_edge = curr_node.children[suffix[curr_letter]]
            interval = curr_edge.interval

            word_letter = interval[0]
            while word_letter <= interval[1]:
                if self.word[word_letter] != suffix[curr_letter]:  # head ended at implicit node, making real node
                    # edge from new node to the to the node at the end of current edge
                    old_edge_interval = (word_letter, interval[1])
                    old_edge = Edge(old_edge_interval, curr_edge.node)

                    # edge from new node to the leaf made for current suffix
                    new_edge_interval = (len(self.word) - len(suffix) + curr_letter, len(self.word)-1)
                    new_edge = Edge(new_edge_interval, Node())

                    # new node in the place where was just implicit node
                    new_node = Node()
                    new_node.add_child(self.word[old_edge.interval[0]], old_edge)
                    new_node.add_child(self.word[new_edge.interval[0]], new_edge)

                    # current edge is shortened: now it is from current node to new node
                    curr_edge_interval = (interval[0], word_letter-1)
                    curr_edge = Edge(curr_edge_interval, new_node)
                    curr_node.add_child(self.word[interval[0]], curr_edge)

                    # to leave both loops
                    curr_letter = len(suffix)
                    break

                word_letter += 1
                curr_letter += 1
            else:
                curr_node = curr_node.children[self.word[interval[0]]].node

        else:   # head ended at the node
            if curr_letter < len(suffix):
                # making new edge from current node to the leaf
                new_edge_interval = (len(self.word) - len(suffix) + curr_letter, len(self.word) - 1)
                new_edge = Edge(new_edge_interval, Node())

                curr_node.add_child(suffix[curr_letter], new_edge)

    def find(self, word):
        curr_letter = 0
        curr_node = self.root
        while curr_letter < len(word):
            # checking if common part of word to find and text represented by the tree ended in the current node
            if word[curr_letter] not in curr_node.children:
                return False

            # looking for edge which is going out from current node
            curr_edge = curr_node.children[word[curr_letter]]
            interval = curr_edge.interval

            # checking current edge
            word_letter = interval[0]
            while word_letter <= interval[1]:
                if curr_letter == len(word):
                    return True

                if self.word[word_letter] != word[curr_letter]:
                    return False

                curr_letter += 1
                word_letter += 1

            curr_node = curr_edge.node

        return True

    @property
    def root(self):
        return self._root

    @property
    def word(self):
        return self._word


class Node:
    def __init__(self):
        self._children = {}

    def add_child(self, letter, edge):
        self._children[letter] = edge

    @property
    def children(self):
        return self._children


class Edge:
    def __init__(self, interval, node):
        self._interval = interval
        self._node = node

    @property
    def interval(self):
        return self._interval

    @property
    def node(self):
        return self._node


def simple_mccreight(word):
    tree = Tree(word)
    for i in range(len(word)):
        tree.add_suffix(word[i:])

    return tree
