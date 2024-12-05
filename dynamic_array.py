# Name:Alan Nortey
# OSU Email:noretya@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 2024-04-29
# Description: Abstract Data Types


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Method to resize an array. If current capacity is
         less than or equal to current size, a new array is created with new capacity.
        """
        if new_capacity > 0 and new_capacity >= self._size:
            # Create a new StaticArray with the new capacity
            new_data = StaticArray(new_capacity)

            for index in range(self.length()):
                # Get value at index
                value = self.get_at_index(index)
                new_data.set(index, value)
            self._capacity = new_capacity
            self._data = new_data

    def append(self, value: object) -> None:
        """
        Method appends values to the end of an array. If there is no room to append array
        the capacity is double and the value is appended
        """

        # Check whether there is room for value to be appended
        if self._size < self._capacity:
            self._data[self._size] = value
            self._size += 1

            # If there is no room for value to be added double capacity and append value
        else:
            self.resize(2 * self._capacity)
            self._data[self._size] = value
            self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts values at a specific index.
        Increases size of original index.
        """
        if index < 0 or index > self._size:
            raise DynamicArrayException('Index out of bounds')

        if self._size == self._capacity:  # If array is full, double the capacity
            self.resize(2 * self._capacity)

        # Shift elements to make space for the new value
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

        # Insert the value at the specified index
        self._data[index] = value
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Removes the element at the specified index in the dynamic array.
        """
        # If an invalid index is given, raise a DynamicArrayException
        if index < 0 or index > self._size - 1:
            raise DynamicArrayException

            # Check the size against the capacity, if already full, double the capacity.
        if self._size < self._capacity/4 and self._capacity > 10:
            if 10 <= int(self._capacity / 2):
                self.resize(int(self._size * 2))
            else:
                self.resize(10)

        # Shift array and add replace value
        for original_index in range(self._size - index - 1):
            shift_index = original_index + index
            value = self.get_at_index(shift_index + 1)
            self.set_at_index(shift_index, value)

        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Create an array that is a slice of a parent array. The slice array starts from start
        index and moves ends at start index+index
        """
        # Validate that inputs are not less than 0
        if size < 0 or start_index < 0:
            raise DynamicArrayException

        # Validate that inputs are  greater than length of array
        if start_index > self._size - 1 or start_index + size > self._size:
            raise DynamicArrayException

        sliced_array = DynamicArray()
        for original_index in range(size):
            # Get value sliced from original array
            sliced_value = self.get_at_index(original_index+start_index)
            sliced_array.insert_at_index(original_index, sliced_value)

        return sliced_array

    def map(self, map_func) -> "DynamicArray":
        """
        Map method applies a specified function to each item of an iterable list.
        """
        map_array = DynamicArray()

        for index in range(self._size):

            # Get value at index
            value = self.get_at_index(index)

            # Insert value into map_array and perform function on it.
            map_array.insert_at_index(index, map_func(value))
        return map_array

    def filter(self, filter_func) -> "DynamicArray":

        """
        Method creates a new dynamic array populated only with those elements from the
        original array
        """
        filtered_array = DynamicArray()

        for index in range(self._size):
            value = self.get_at_index(index)
            if filter_func(value):
                filtered_array.append(value)
        return filtered_array

    def reduce(self, reduce_func, initializer=None) -> object:

        """
        Method  iterates through the array and applies the reduce_func to each element.
        """
        # Initializer is set to the first value if array is set as initializer
        if initializer == None:
            shift = 1
        else: shift = 0
        if initializer == None and self._size>0:
            default_initializer = self.get_at_index(0)
        else:
            default_initializer = initializer

        for index in range(self._size-shift):
            value = self.get_at_index(index+shift)
            default_initializer = reduce_func(default_initializer, value)

        return default_initializer



def chunk(arr: DynamicArray) -> DynamicArray:
    """
    Chunks a DynamicArray into non-descending subsequences.
    Returns a DynamicArray of DynamicArrays.
    """
    chunked_array = DynamicArray()

    if arr.is_empty():
        return chunked_array

    current_chunk = DynamicArray()
    current_chunk.append(arr[0])

    for i in range(1, arr.length()):
        if arr[i] >= current_chunk[current_chunk.length() - 1]:
            current_chunk.append(arr[i])
        else:
            chunked_array.append(current_chunk)
            current_chunk = DynamicArray()
            current_chunk.append(arr[i])

    chunked_array.append(current_chunk)

    return chunked_array


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:

    """
    This method finds the mode of an array and returns a tuple of
    the mode element and the frequency it occurred.
    """
    # Initialize frequency and count.
    frequency = 1
    count = 1
    mode_array = DynamicArray()
    array_length = arr.length()

    for index in range(array_length):
        value = arr.get_at_index(index)
        if index < array_length - 1:
            next_value = arr.get_at_index(index + 1)
        else:
            next_value = None

        if value == next_value:
            count += 1
        else:
            count = 1

        if count > frequency:
            frequency = count
            mode_array = arr.slice(0, 0)
            mode_array.append(value)
        elif count == frequency:
            mode_array.append(value)

    return mode_array, frequency



# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    def print_chunked_da(arr: DynamicArray):
        if len(str(arr)) <= 100:
            print(arr)
        else:
            print(f"DYN_ARR Size/Cap: {arr.length()}/{arr.get_capacity()}")
            print('[\n' + ',\n'.join(f'\t{chunk}' for chunk in arr) + '\n]')

    print("\n# chunk example 1")
    test_cases = [
        [10, 20, 30, 30, 5, 10, 1, 2, 3, 4],
        ['App', 'Async', 'Cloud', 'Data', 'Deploy',
         'C', 'Java', 'Python', 'Git', 'GitHub',
         'Class', 'Method', 'Heap']
    ]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# chunk example 2")
    test_cases = [[], [261], [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
