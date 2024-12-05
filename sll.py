# Name:Alan Nortey
# OSU Email:noretya@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 2024-05-6
# Description: Singly Linked List


from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        Inserts a value at the front of the Linked List
        """
        # Define the next value following the  value to be inserted
        front_sentinel = self._head

        # Create a new node  with value and next value pointer

        new_node = SLNode(value, front_sentinel.next)
        front_sentinel.next = new_node

        # Replace the head value with the  New Node



    def insert_back(self, value: object) -> None:
        """
        Insert a node at the  end of a Linked List
        """
        back_sentinel = self._head
        new_node = SLNode(value)

        # Locate the last node in the linked list
        while back_sentinel.next is not None:
            back_sentinel = back_sentinel.next

        # Update the last node's next pointer to point to the new node
        back_sentinel.next = new_node




    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts a value at a specific index in a linked list.
        """
        # Check if index is negative or bigger that data size(length).
        if index < 0 or index > self.length():
            raise SLLException

        current_node = self._head
        new_node = SLNode(value)
        # Move through node until insertion location
        for i in range(index):
            current_node = current_node.next

        # Insert value pointer to next value
        new_node.next = current_node.next

        current_node.next = new_node





    def remove_at_index(self, index: int) -> None:
        """
        Remove node value from a specified index
        """

        # Check if index is negative or bigger that data size(length) or empty.
        if index < 0 or index+1 > self.length() or self.length() ==0:
            raise SLLException


        # Initialize Previous node to none

        previous_node = None
        current_node = self._head

        # Go through node to the index at the specified position
        for i in range(index+1):
            previous_node = current_node
            current_node = current_node.next

        # Remove the node by skipping pointer to next node
        previous_node.next = current_node.next



    def remove(self, value: object) -> bool:
        """
        Remove value from a singly linked list
        """
        front_sentinel = self._head
        current_node = front_sentinel.next
        previous_node = None

        if self.length() == 0:
            return False

        while current_node is not None:
            if current_node.value == value:
                if previous_node is not None:
                    previous_node.next = current_node.next
                else:
                    front_sentinel.next = current_node.next
                return True
            previous_node = current_node
            current_node = current_node.next

        return False




    def count(self, value: object) -> int:
        """
        Counts occurrence of specific value in a Linked list.
        """

        front_sentinel = self._head
        current_node = front_sentinel.next
        counter = 0

        if self.length() ==0:
            return 0

        for i in range(self.length()):
            if current_node.value == value:
                counter += 1

            # Move to next node on the list
            current_node = current_node.next
        return counter


    def find(self, value: object) -> bool:
        """
        Find a value in a Linked List.
        """

        front_sentinel = self._head
        current_node = front_sentinel.next

        for i in range(self.length()):
            if current_node.value == value:
                return True

            current_node = current_node.next
        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        Creates a new Linked List that contains the requested number of nodes from the
        original list, starting with the node located at the requested start index.
        """

        if start_index < 0 or start_index >= self.length() or size < 0 or start_index + size > self.length():
            raise SLLException

        new_list = LinkedList()
        current_node = self._head.next
        new_head = None
        prev_node = None

        for i in range(self.length()):
            if i >= start_index and i < start_index + size:
                new_node = SLNode(current_node.value)
                if new_head is None:
                    new_head = new_node
                if prev_node is not None:
                    prev_node.next = new_node
                prev_node = new_node
            current_node = current_node.next

        new_list._head.next = new_head
        new_list._size = size

        return new_list


if __name__ == "__main__":

    print("\n# insert_front example 1")
    test_case = ["A", "B", "C"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_front(case)
        print(lst)

    print("\n# insert_back example 1")
    test_case = ["C", "B", "A"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_back(case)
        print(lst)

    print("\n# insert_at_index example 1")
    lst = LinkedList()
    test_cases = [(0, "A"), (0, "B"), (1, "C"), (3, "D"), (-1, "E"), (5, "F")]
    for index, value in test_cases:
        print("Inserted", value, "at index", index, ": ", end="")
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove_at_index example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"Initial LinkedList : {lst}")
    for index in [0, 2, 0, 2, 2, -2]:
        print("Removed at index", index, ": ", end="")
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [7, 3, 3, 3, 3]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# remove example 2")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# count example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print("\n# find example 1")
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    print(lst)
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")
