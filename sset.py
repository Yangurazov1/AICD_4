#!/usr/bin/env python3

"""
Suffix tree to search in dictionary
"""

from typing import List, Tuple

class Node:
    def __init__(self, char: str, parent: 'Node' = None):
        self.char = char
        self.parent = parent
        self.children: List[Node] = []
        self.suffix_link: Node = None
        self.index: int = -1

class SuffixTree:
    def __init__(self):
        self.root = Node(None)
        self.active_node = self.root
        self.active_length = 0
        self.remainder = ''

    def add_string(self, string: str, index: int):
        for char in string:
            self.add_char(char, index)

    def add_char(self, char: str, index: int):
        new_node = Node(char, self.active_node)
        self.active_node.children.append(new_node)
        new_node.index = index

        if self.active_length > 0:
            self.active_length -= 1
            self.active_node = self.active_node.suffix_link

        if self.active_node != self.root:
            failure_node = self.active_node.suffix_link
            while failure_node is not None and failure_node.find(self.remainder + char) is None:
                failure_node = failure_node.suffix_link
            if failure_node is not None:
                new_node.suffix_link = failure_node.find(self.remainder + char)
            else:
                new_node.suffix_link = self.root

        self.remainder += char
        if len(self.remainder) > self.active_length + 1:
            self.remainder = self.remainder[1:]

        self.active_length += 1
        self.active_node = new_node

    def find(self, string: str) -> Node:
        node = self.root
        for char in string:
            node = node.find(char)
            if node is None:
                return None
        return node

class SSet:
    """String set. Should be based on Suffix tree"""

    def __init__(self, fname: str) -> None:
        """Saves filename of a dictionary file"""
        self.tree = SuffixTree()
        self.words = []
        self.fname = fname

    def load(self) -> None:
        """
        Loads words from a dictionary file.
        Each line contains a word.
        File is not sorted.
        """
        with open(self.fname, 'r') as f:
            for i, line in enumerate(f):
                self.words.append(line.rstrip())
                self.tree.add_string(line.rstrip(), i)

    def search(self, substring: str) -> List[str]:
        """Returns all words that contain substring."""
        node = self.tree.find(substring)
        if node is None:
            return []
        words = []
        while node is not None:
            if node.index != -1:
                words.append(self.words[node.index])
            node = node.suffix_link
        return words

