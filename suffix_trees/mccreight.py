class Tree:
    """Structure containing suffix tree"""
    def __init__(self, word):
        self._root = Node(None, "")
        self._word = word

    def split_edge(self, parent_node, top_interval):
        # current edge
        curr_edge = parent_node.children[self.word[top_interval[0]]]

        # new node
        new_node = Node(parent_node, self.word[top_interval[0]])

        # edge from parent node to the new node
        top_edge = Edge(top_interval, new_node)
        parent_node.children[self.word[top_interval[0]]] = top_edge

        # edge from new node to the child of parent node
        bottom_interval = (top_interval[1] + 1, curr_edge.interval[1])
        bottom_edge = Edge(bottom_interval, curr_edge.node)
        new_node.add_child(self.word[top_interval[1] + 1], bottom_edge)
        curr_edge.node.parent = new_node
        curr_edge.node.parent_first_letter = self.word[top_interval[1] + 1]

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
    def __init__(self, parent, parent_first_letter):
        self._parent = parent
        self._parent_first_letter = parent_first_letter
        self._children = {}

        self._link = None

    def add_child(self, letter, edge):
        self._children[letter] = edge

    def print(self):
        print(self._children)
        for child in self._children.values():
            print(child.interval)
            child.node.print()

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @property
    def parent_first_letter(self):
        return self._parent_first_letter

    @property
    def link(self):
        return self._link

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @parent_first_letter.setter
    def parent_first_letter(self, parent_first_letter):
        self._parent_first_letter = parent_first_letter

    @link.setter
    def link(self, link):
        self._link = link


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


def split_edge(parent_node, top_interval, word):
    # current edge
    curr_edge = parent_node.children[word[top_interval[0]]]

    # new node
    new_node = Node(parent_node, word[top_interval[0]])

    # edge from parent node to the new node
    top_edge = Edge(top_interval, new_node)
    parent_node.children[word[top_interval[0]]] = top_edge

    # edge from new node to the child of parent node
    bottom_interval = (top_interval[1] + 1, curr_edge.interval[1])
    bottom_edge = Edge(bottom_interval, curr_edge.node)
    new_node.add_child(word[top_interval[1] + 1], bottom_edge)
    curr_edge.node.parent = new_node
    curr_edge.node.parent_first_letter = word[top_interval[1] + 1]


def graft(node, interval, first_letter):
    new_node = Node(node, first_letter)
    new_edge = Edge(interval, new_node)
    node.add_child(first_letter, new_edge)

    return new_node


def label_size(label):
    return label[1] - label[0] + 1


def fast_find(node, label, word):
    curr_node = node
    curr_label = label

    child_edge = curr_node.children[word[curr_label[0]]]
    while label_size(curr_label) > label_size(child_edge.interval):
        curr_node = child_edge.node
        curr_label = (curr_label[0] + label_size(child_edge.interval), curr_label[1])

        child_edge = curr_node.children[word[curr_label[0]]]

    if label_size(curr_label) == label_size(child_edge.interval):
        return child_edge.node
    else:
        new_node_top_label = (child_edge.interval[0], child_edge.interval[0] + label_size(curr_label) - 1)
        split_edge(curr_node, new_node_top_label, word)

        curr_node = curr_node.children[word[curr_label[0]]].node

        return curr_node


def slow_find(node, label, word):
    curr_node = node
    curr_label_letter = label[0]

    if not word[curr_label_letter] in curr_node.children:
        return curr_node, label

    child_edge = curr_node.children[word[curr_label_letter]]
    curr_edge_letter = child_edge.interval[0]

    while word[curr_label_letter] == word[curr_edge_letter]:
        if curr_edge_letter == child_edge.interval[1]:
            curr_node = child_edge.node
            curr_label_letter += 1
            if not word[curr_label_letter] in curr_node.children:
                return curr_node, (curr_label_letter, label[1])

            child_edge = curr_node.children[word[curr_label_letter]]
            curr_edge_letter = child_edge.interval[0]
        else:
            curr_label_letter += 1
            curr_edge_letter += 1

    new_node_top_interval = (child_edge.interval[0], curr_edge_letter - 1)
    split_edge(curr_node, new_node_top_interval, word)

    left_label = (curr_label_letter, label[1])
    return curr_node.children[word[child_edge.interval[0]]].node, left_label


def mccreight(word):
    tree = Tree(word)
    head = tree.root
    node = tree.root
    leaf = graft(node, (0, len(word)-1), word[0])

    for i in range(1, len(word)):
        left_label = (i, len(word)-1)
        if head == tree.root:
            node = tree.root
        else:
            to_head_label = head.parent.children[head.parent_first_letter].interval

            if head.parent == tree.root:
                to_head_label = (to_head_label[0] + 1, to_head_label[1])

                node = tree.root
            else:
                node = head.parent.link

            if to_head_label[1] >= to_head_label[0]:
                node = fast_find(node, to_head_label, word)
            left_label = (leaf.parent.children[leaf.parent_first_letter].interval[0], left_label[1])

        last_head = head
        head, left_label = slow_find(node, left_label, word)
        last_head.link = node
        leaf = graft(head, left_label, word[left_label[0]])

    return tree
