# Name:Alan Nortey
# OSU Email:noretya@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 2024-05-28
# Description: Heap Implementation


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MinHeap with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MinHeap content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return "HEAP " + str(heap_data)

    def add(self, node: object) -> None:
        """
        Adds a new value to a min heap
        """
    # Add value to the heap array
        self._heap.append(node)
    # Index of the node value in the heap array. Start from last value
        current_node_index = self._heap.length()-1
        parent_node_index = (current_node_index-1)//2

        while current_node_index > 0 and self._heap.get_at_index(current_node_index) <\
                self._heap.get_at_index(parent_node_index):
            # Switch parent node and if node is less the added node
            self._heap[current_node_index], self._heap[parent_node_index] = \
                self._heap[parent_node_index], self._heap[current_node_index]
            # Set  node to parent node
            current_node_index = parent_node_index
            parent_node_index = (current_node_index-1)//2

    def is_empty(self) -> bool:
        """
        Method checks if heap is empty. Returns True if is heap is empty.
        Returns False if heap is no empty.
        """
        return self._heap.length() == 0

    def get_min(self) -> object:
        """
        Get the Min value of the heap array
        """
        # If heap array is empty raise exception
        if self._heap.length() == 0:
            raise MinHeapException
        else:
            return self._heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Method removes the minimum value from the heap and returns it.
        Raises MinHeapException if the heap is empty.
        """
        if self._heap.is_empty():
            raise MinHeapException

        # Swap the root node (minimum) with the last node
        self._heap[0], self._heap[self._heap.length() - 1] = self._heap[self._heap.length() - 1], self._heap[0]
        min_value = self._heap[self._heap.length() - 1]
        # Remove the last node (minimum value)
        self._heap.remove_at_index(self._heap.length() - 1)

        # Percolate down from the root to restore the heap property
        current = 0
        while current < self._heap.length():
            left_child = 2 * current + 1
            right_child = 2 * current + 2

            # Check if left child exists
            if left_child < self._heap.length():
                # Check if right child exists and is smaller
                if right_child < self._heap.length() and self._heap[right_child] < self._heap[left_child]:
                    min_child = right_child
                else:
                    min_child = left_child
                # Swap with the smaller child if it's smaller than the current node
                if self._heap[min_child] < self._heap[current]:
                    self._heap[current], self._heap[min_child] = self._heap[min_child], self._heap[current]
                    current = min_child
                else:
                    break
            else:
                break

        return min_value

    def _percolate_down(self, da: DynamicArray, parent: int) -> None:
        """
        Method moves down heap Dynamic array, da, from index, parent.
        """
        size = da.length()

        while parent >= 0:
            left_child = 2 * parent + 1
            right_child = 2 * parent + 2

            # Find the index of the smaller child (if it exists)
            if right_child < size and da[right_child] < da[left_child]:
                smaller_child = right_child
            else:
                # If the right child doesn't exist, or greater than parent, use the left child
                if left_child < size:
                    smaller_child = left_child
                else:
                    # If both children don't exist, set smaller_child to -1 to indicate no smaller child
                    smaller_child = -1

            # If there is a smaller child, and it's smaller than the parent, swap
            if smaller_child != -1 and da[smaller_child] < da[parent]:
                da[parent], da[smaller_child] = da[smaller_child], da[parent]
                parent = smaller_child
            else:
                break

    def build_heap(self, da: DynamicArray) -> None:
        """
        Builds a proper MinHeap from the given DynamicArray.
        Overwrites the current content of the MinHeap.
        """
        # Copy the elements of the DynamicArray into the MinHeap
        self._heap = DynamicArray(da)

        #  Percolate value starting from the last non-leaf  heap node up to the root
        # Start from the parent of the last node (index: (length of array // 2 )- 1) and go towards the root
        for i in range(da.length() // 2 - 1, -1, -1):
            self._percolate_down(self._heap, i)

    def size(self) -> int:
        """
        Method find the number of values in a heap array
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Method clears all the entries in a heap
        """
        self._heap = DynamicArray()
        return



def left(i):
    """ Method for left  index of a heap"""
    return 2 * i + 1

def right(i):
    """Method for right index of a heap"""
    return 2 * i + 2


def _percolate_down(a:DynamicArray, n: int, i: int) -> None:
    """
    Perform a trickle-down operation on the heap.

    """
    # n is length of the array
    # Keep trickling down until the index is within the bounds of the array
    while i >= 0:
        j = -1
        r = right(i)  # Get the index of the right child of node i
        # Check if the right child exists and is smaller than the current node
        if r < n and a[r] < a[i]:
            l = left(i)  # Get the index of the left child of node i
            # Determine which child (left or right) is smaller
            if a[l] < a[r]:
                j = l  # Assign the index of the left child to j
            else:
                j = r  # Assign the index of the right child to j
        else:
            l = left(i)  # Get the index of the left child of node i
            # Check if the left child exists and is smaller than the current node
            if l < n and a[l] < a[i]:
                j = l  # Assign the index of the left child to j
        # If a smaller child was found, swap the current node with it
        if j >= 0:
            a[j], a[i] = a[i], a[j]
        i = j  # Move to the next level down in the heap

def heapsort(da: DynamicArray) -> None:
    """
    Sorts the given DynamicArray using the heap sort algorithm.
    """
    n = da.length()  # Get the length of the DynamicArray
    m = n // 2  # Calculate the midpoint of the DynamicArray
    # Build the heap by performing trickle-down operations on non-leaf nodes
    for i in range(m - 1, -1, -1):
        _percolate_down(da, n, i)
    # Repeatedly extract the minimum element from the heap and restore the heap property
    while n > 1:
        n -= 1
        da[n], da[0] = da[0], da[n]  # Swap the root (minimum element) with the last element
        _percolate_down(da, n, 0)  # Restore the heap property starting from the root





# ----------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
