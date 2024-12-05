# Name:Alan Nortey
# OSU Email:norteya@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment:4
# Due Date:2024-05-20
# Description: Binary Search Tree and AVL implementation.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Add a node value to the AVL
        """
        # Create a new AVLNode with the given value
        new_node = AVLNode(value)

        # If the AVL tree is empty, set the new node as the root
        if self._root is None:
            self._root = new_node
            return

        # Find the position to insert the new node
        current_node = self._root
        while current_node is not None:
            if value == current_node.value:
                # Duplicate value, do not add to the tree
                return
            elif value < current_node.value:
                if current_node.left is None:
                    current_node.left = new_node
                    new_node.parent = current_node
                    break
                else:
                    current_node = current_node.left
            else:
                if current_node.right is None:
                    current_node.right = new_node
                    new_node.parent = current_node
                    break
                else:
                    current_node = current_node.right

        # Rebalance the tree starting from the parent of the new node
        self._rebalance(new_node.parent)

    def remove(self, value: object) -> bool:
        """
        Remove a node from the AVL tree.
        Return True if the node was removed.
        Return False if the node was not found.
        """

        # Helper function to find the node to remove and its parent
        def find_node_to_remove(value):
            current_node = self._root
            parent_node = None
            while current_node is not None and current_node.value != value:
                parent_node = current_node
                if value < current_node.value:
                    current_node = current_node.left
                else:
                    current_node = current_node.right
            return current_node, parent_node

        # Find the node to remove and its parent
        node_to_remove, parent_of_node_to_remove = find_node_to_remove(value)

        # If the node to remove is not found, return False
        if node_to_remove is None:
            return False

        # Node with two children: Get the in-order successor (smallest in the right subtree)
        if node_to_remove.left is not None and node_to_remove.right is not None:
            successor = node_to_remove.right
            successor_parent = node_to_remove
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            # Replace the value of the node to be removed with the value of the successor
            node_to_remove.value = successor.value
            # Update node_to_remove to be successor
            node_to_remove = successor
            parent_of_node_to_remove = successor_parent

        # Node with zero or one child
        if node_to_remove.left is None:
            child = node_to_remove.right
        else:
            child = node_to_remove.left

        # Remove node_to_remove from the tree
        if parent_of_node_to_remove is None:  # Removing the root node
            self._root = child
        elif parent_of_node_to_remove.left == node_to_remove:
            parent_of_node_to_remove.left = child
        else:
            parent_of_node_to_remove.right = child

        # Rebalance the tree starting from the parent of the removed node
        self._rebalance(parent_of_node_to_remove)

        return True

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Removes two subtrees from a AVL
        """
        # Find the inorder successor and its parent
        successor = remove_node.right
        successor_parent = remove_node
        while successor.left is not None:
            successor_parent = successor
            successor = successor.left

        # Replace the value of the node to be removed with the value of the inorder successor
        remove_node.value = successor.value

        # Determine which child of the successor_parent the successor is and update the appropriate reference
        if successor_parent.left == successor:
            successor_parent.left = successor.right
        else:
            successor_parent.right = successor.right

        # Rebalance the tree starting from the parent of the removed node
        if remove_parent is None:
            self._rebalance(self._root)
        else:
            self._rebalance(remove_parent)

        return self._root

                #

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Finds the balance factor for a Node in AVL
        """
        if node is None:
            return 0
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        return right_height - left_height

    def _get_height(self, node: AVLNode) -> int:
        """
        Gets height between the left and right nodes
        """
        if node is None:
            return -1
        return max(self._get_height(node.left), self._get_height(node.right)) + 1

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Performs a left rotation on a Node to maintain BST
        """
        new_root = node.right
        node.right = new_root.left
        if new_root.left:
            new_root.left.parent = node
        new_root.parent = node.parent
        if node.parent is None:
            self._root = new_root
        elif node == node.parent.left:
            node.parent.left = new_root
        else:
            node.parent.right = new_root
        new_root.left = node
        node.parent = new_root

        # Update heights
        self._update_height(node)
        self._update_height(new_root)

        return new_root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Performs a right rotation on a Node to maintain BST
        """
        new_root = node.left
        node.left = new_root.right
        if new_root.right:
            new_root.right.parent = node
        new_root.parent = node.parent
        if node.parent is None:
            self._root = new_root
        elif node == node.parent.right:
            node.parent.right = new_root
        else:
            node.parent.left = new_root
        new_root.right = node
        node.parent = new_root

        # Update heights
        self._update_height(node)
        self._update_height(new_root)

        return new_root

    def _update_height(self, node: AVLNode) -> None:
        """
        Updates the height of the node when rotation is done
        """
        if node is not None:
            left_height = self._get_height(node.left)
            right_height = self._get_height(node.right)
            node.height = max(left_height, right_height) + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Updates the height of a node and performs sets new balance factor.
        """
        while node is not None:
            # Update the height of the current node
            self._update_height(node)

            # Calculate the balance factor of the current node
            balance_factor = self._balance_factor(node)

            # Perform rotations if necessary
            if balance_factor > 1:  # Right subtree is heavier
                if self._balance_factor(node.right) < 0:
                    # Right-left case: Perform a right rotation on the right child, then a left rotation on the node
                    node.right = self._rotate_right(node.right)
                # Perform a left rotation on the node
                node = self._rotate_left(node)
            elif balance_factor < -1:  # Left subtree is heavier
                if self._balance_factor(node.left) > 0:
                    # Left-right case: Perform a left rotation on the left child, then a right rotation on the node
                    node.left = self._rotate_left(node.left)
                # Perform a right rotation on the node
                node = self._rotate_right(node)

            # Move up to the parent of the current node
            node = node.parent

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)


    print("\nText 2")
    my_tree= AVL([42, 57, 49, 22, 75, 32, 88, 44, 47])
