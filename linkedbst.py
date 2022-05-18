"""
File: linkedbst.py
Author: Ken Lambert
"""
import math
import random
import time

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """A link-based binary search tree implementation."""

    def __init__(self, source_collection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, source_collection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            res = ""
            if node is not None:
                res += recurse(node.right, level + 1)
                res += "| " * level
                res += str(node.data) + "\n"
                res += recurse(node.left, level + 1)
            return res

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return lyst

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    @staticmethod
    def is_leaf(curr_node):
        """
        Checks whether a node is a leaf in a tree.
        """
        return curr_node.left is None and curr_node.right is None

    def height(self):
        """
        Return the height of tree
        :return: int
        """
        heights = []

        def recurse(curr_node=self._root, height=0):
            if self.is_leaf(curr_node):
                heights.append(height)
            else:
                height += 1
                if curr_node.left is not None:
                    recurse(curr_node.left, height)
                if curr_node.right is not None:
                    recurse(curr_node.right, height)

        recurse()
        return max(heights)

    def is_balanced(self):
        """
        Returns True if tree is balanced.
        :return:
        """
        return self.height() < 2 * math.log2(self._size + 1) - 1

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high."""
        lst = self.inorder()
        return [elem for elem in lst if low <= elem <= high]

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """
        res = self.inorder()
        self.clear()

        def traversal(lst: list):
            """
            A traversal of the tree.
            """
            if not lst:
                return
            middle = len(lst) // 2
            self.add(lst[middle])
            traversal(lst[:middle])
            traversal(lst[middle + 1:])

        traversal(res)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = self.inorder()
        for elem in lst:
            if elem > item:
                return elem

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = self.inorder()
        for elem in list(reversed(lst)):
            if elem < item:
                return elem

    @staticmethod
    def demo_bst(path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words = []
        with open(path) as file:
            words = file.readlines()
        words = [elem[:-1] for elem in words]
        random_words = [random.choice(words) for _ in range(10 ** 4)]
        start = time.perf_counter()
        for word in random_words:
            words.index(word)
        end = time.perf_counter()
        print(f"List: {end - start} seconds")
        tree = LinkedBST(words[:1000])
        start = time.perf_counter()
        for word in random_words:
            tree.find(word)
        end = time.perf_counter()
        print(f"Unbalanced tree: {(end - start) * (len(words) // 1000)} seconds.")
        words_new = random.sample(words, len(words))
        tree = LinkedBST(words_new)
        start = time.perf_counter()
        for word in random_words:
            tree.find(word)
        end = time.perf_counter()
        print(f"Unbalanced tree (shuffled list): {(end - start)} seconds.")
        tree.rebalance()
        start = time.perf_counter()
        for word in random_words:
            tree.find(word)
        end = time.perf_counter()
        print(f"Balanced Tree: {(end - start)} seconds.")


def main():
    LinkedBST.demo_bst("words.txt")


if __name__ == "__main__":
    main()
