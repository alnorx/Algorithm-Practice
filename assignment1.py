# Name:Alan Nortey
# OSU Email:norteya@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment:1
# Due Date:2024-4-22
# Description:Assignment for Python Review and Big-O notation.


import random
from static_array import *


# ------------------- PROBLEM 1 - MIN_MAX -----------------------------------

def min_max(arr: StaticArray) -> tuple[int, int]:
    """
    Method takes an array and returns the min and max of the value of the
    array as a tuple.
    """
    # Initial min and max number is first number in the array.
    min_num = arr[0]
    max_num = arr[0]
    length_array = arr.length()
    for i in range(length_array):
        if arr[i] > max_num:
            max_num = arr[i]
        if arr[i] < min_num:
            min_num = arr[i]
    return min_num,max_num

# ------------------- PROBLEM 2 - FIZZ_BUZZ ---------------------------------


def fizz_buzz(arr: StaticArray) -> StaticArray:
    """
    Method takes an array of numbers and determines if the numbers
    are multiple of 3 and 5. Returns fizz if a number in the list is a multiple of 3,
   returns buzz, if a number is a multiple of 5, and fizzbuzz if a number is multiple of 3 and 5
    """

    length_arr = arr.length()
    arr_copy = StaticArray(length_arr)

    for i in range(length_arr):
        # Verify that a number in the original array is a multiple of 3,5 or both.
        # Verify that array entry is not a string or float.
        if arr[i] % 15 == 0 and type(arr[i]) == int:
            arr_copy[i] = "fizzbuzz"
        elif arr[i] % 5 == 0 and type(arr[i]) == int:
            arr_copy[i] = "buzz"
        elif arr[i] % 3 == 0 and type(arr[i]) == int:
            arr_copy[i] = "fizz"
        else:
            arr_copy[i] = arr[i]
    return arr_copy

# ------------------- PROBLEM 3 - REVERSE -----------------------------------


def reverse(arr: StaticArray) -> None:
    length_array = arr.length()
    """
    The method takes an array and returns the reversed array
    """
    for i in range(length_array//2):
        reverse_index = length_array - i - 1
        # Temporary variable to store the values of the last half of array
        temp_variable = arr[reverse_index]
        arr[reverse_index] = arr[i]
        arr[i] = temp_variable

# ------------------- PROBLEM 4 - ROTATE ------------------------------------


def rotate(arr: StaticArray, steps: int) -> StaticArray:

    """
    Method rotates(shifts) array entries by a number of steps.
    Array entries are is shifted to the right if steps integer is positive.
    Array entries are is shifted to the left  if steps  integer is negative.
    """
    length_arr = arr.length()
    arr_copy = StaticArray(length_arr)
    for i in range(length_arr):
        # Shifts to the right if steps is positive.
        if steps >= 0:
            # temp index produces negative index
            temp_index = i - (steps % length_arr)
            shift_index = abs(temp_index + length_arr) % length_arr
            arr_copy[i] = arr[shift_index]

        # Shifts to the left if steps is negative
        else:

            arr_copy[i] = arr[abs((i-steps)%length_arr)]
    return arr_copy

# ------------------- PROBLEM 5 - SA_RANGE ----------------------------------


def sa_range(start: int, end: int) -> StaticArray:
    """
    This method takes two integers, a start and  an end and returns
    an array of numbers, incrementing by one, from the start integer to the end
    integer
    """
    length_arr = abs(start - end)+1
    arr_copy = StaticArray(length_arr)
    for i in range(length_arr):
        # If the starting number is less than the ending number.
        # List is in ascending order
        if start < end:
            arr_copy[i] = start+i

        # If the starting number is greater than the ending number.
        # List is in descending order
        else:
            arr_copy[i] = start-i
    return arr_copy

# ------------------- PROBLEM 6 - IS_SORTED ---------------------------------


def is_sorted(arr: StaticArray) -> int:
    """
    Method returns:
     1 if array is sorted in ascending order
    -1 if array is sorted in descending order
     0 if array is not sorted
    """
    length_arr = arr.length()
    # An array with less than 2 elements is always sorted
    if length_arr < 2:
        return 1

    # Check for ascending order
    ascending = True
    for i in range(1, length_arr):
        if arr[i] < arr[i - 1]:
            ascending = False
            break

    if ascending:
        return 1

    # Check for descending order
    descending = True
    for i in range(1, length_arr):
        if arr[i] > arr[i - 1]:
            descending = False
            break

    if descending:
        return -1

    return 0

# ------------------- PROBLEM 7 - FIND_MODE -----------------------------------


def find_mode(arr: StaticArray) -> tuple[object, int]:
    """
    This method takes array and returns the mode, the most occurring element
    and the number of times it appears in the array.
    """
    length_arr = arr.length()
    max_count = 0
    mode_value = None
    current_count = 1
    current_mode = arr[0]

    for i in range(1, length_arr):
        # Compare array element to previous array element.
        if arr[i] == arr[i - 1]:
            current_count += 1
        else:
            # Replace mode value with current_mode
            if current_count > max_count:
                mode_value = current_mode
                max_count = current_count
            current_count = 1
            current_mode = arr[i]

    # Check the last element
    if current_count > max_count:
        mode_value = current_mode
        max_count = current_count
    return mode_value, max_count

# ------------------- PROBLEM 8 - REMOVE_DUPLICATES -------------------------


def remove_duplicates(arr: StaticArray) -> StaticArray:
    """
    Method takes an array and removes the duplicate elements.
    Returns an array of the unique elements in the original array.
    """
    unique_count = 1  # Initialize with 1 to account for the first element
    for i in range(1, arr.length()):
        if arr[i] != arr[i - 1]:
            unique_count += 1

    # Create a new StaticArray with the size of unique elements
    unique_arr = StaticArray(unique_count)

    # Initialize a variable to keep track of the index in the new StaticArray
    unique_index = 0

    # Iterate through the array starting from the second element
    for i in range(1, arr.length()):
        # If the current element is different from the previous one, add it to unique_arr
        if arr[i] != arr[i - 1]:
            unique_arr[unique_index] = arr[i - 1]
            unique_index += 1

    # Add the last element of the array (since it's not checked in the loop)
    unique_arr[unique_index] = arr[arr.length() - 1]

    return unique_arr
# ------------------- PROBLEM 9 - COUNT_SORT --------------------------------

def count_sort(arr: StaticArray) -> StaticArray:

    """
    Performs counting sort on array of numbers in an non-ascending order

    """
    # Find the minimum and maximum values in the array
    # Initial min and max number is first number in the array.
    min_num = arr[0]
    max_num = arr[0]
    length_arr = arr.length()
    for i in range(length_arr):
        if arr[i] > max_num:
            max_num = arr[i]
        if arr[i] < min_num:
            min_num = arr[i]

    # Compute the range of values
    k = max_num - min_num + 1

    # Initialize count array to store frequency of each element
    count = StaticArray(k)
    for i in range(k):
        count[i] = 0

    # Count the occurrences of each element
    for i in range(length_arr):
        count_index=arr[i]-min_num
        count[count_index] += 1

    # Find the  prefix sum of count array
    for i in range(1, k):
        count[i] += count[i - 1]

    # Create a new StaticArray to store the sorted elements
    sorted_arr = StaticArray(arr.length())

    # Iterate through the input array in reverse order to maintain stability
    for i in range(length_arr - 1, -1, -1):
        count_index = arr[i] - min_num
        sorted_arr[length_arr - count[count_index]] = arr[i]
        count[count_index] -= 1

    return sorted_arr
# ------------------- PROBLEM 10 - SORTED SQUARES ---------------------------


def sorted_squares(arr: StaticArray) -> StaticArray:
    """
    Method takes an array of numbers and returns the square of the array in non-descending order.
    """
    length_arr = arr.length()
    # index of sorted min value
    min_index = 0
    max_index = length_arr - 1
    max_value = arr[max_index]
    min_value = arr[min_index]
    # Index of max value in sorted square
    max_index = length_arr - 1

    squared_arr = StaticArray(length_arr)

    for i in range(length_arr - 1, -1, -1):
        # Compare value on first index to last index
        if abs(arr[min_index]) > abs(arr[max_index]):
            squared_arr[i] = arr[min_index] ** 2
            min_index += 1
        else:
            squared_arr[i] = arr[max_index] ** 2
            max_index -= 1
    return squared_arr


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print('\n# min_max example 1')
    arr = StaticArray(5)
    for i, value in enumerate([7, 8, 6, -5, 4]):
        arr[i] = value
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]: 3}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 2')
    arr = StaticArray(1)
    arr[0] = 100
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 3')
    test_cases = (
        [3, 3, 3],
        [-10, -30, -5, 0, -10],
        [25, 50, 0, 10],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        result = min_max(arr)
        if result:
            print(f"Min: {result[0]: 3}, Max: {result[1]}")
        else:
            print("min_max() not yet implemented")

    print('\n# fizz_buzz example 1')
    source = [_ for _ in range(-5, 20, 4)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# reverse example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [1, 2, 0, -1, -2, 28, -100, 2 ** 28, -2 ** 31]:
        space = " " if steps >= 0 else ""
        print(f"{rotate(arr, steps)} {space}{steps}")
    print(arr)

    print('\n# rotate example 2')
    array_size = 1_000_000
    source = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(f'Started rotating large array of {array_size} elements')
    rotate(arr, 3 ** 14)
    rotate(arr, -3 ** 15)
    print(f'Finished rotating large array of {array_size} elements')

    print('\n# sa_range example 1')
    cases = [
        (1, 3), (-1, 2), (0, 0), (0, -3),
        (-95, -89), (-89, -95)]
    for start, end in cases:
        print(f"Start: {start: 4}, End: {end: 4}, {sa_range(start, end)}")

    print('\n# is_sorted example 1')
    test_cases = (
        [-100, -8, 0, 2, 3, 10, 20, 100],
        ['A', 'B', 'Z', 'a', 'z'],
        ['Z', 'T', 'K', 'A', '5'],
        [1, 3, -10, 20, -30, 0],
        [-10, 0, 0, 10, 20, 30],
        [100, 90, 0, -90, -200],
        ['apple']
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        result = is_sorted(arr)
        space = "  " if result and result >= 0 else " "
        print(f"Result:{space}{result}, {arr}")

    print('\n# find_mode example 1')
    test_cases = (
        [1, 20, 30, 40, 500, 500, 500],
        [2, 2, 2, 2, 1, 1, 1, 1],
        ["zebra", "sloth", "otter", "otter", "moose", "koala"],
        ["Albania", "Belgium", "Chile", "Denmark", "Egypt", "Fiji"]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value

        result = find_mode(arr)
        if result:
            print(f"{arr}\nMode: {result[0]}, Frequency: {result[1]}\n")
        else:
            print("find_mode() not yet implemented\n")

    print('# remove_duplicates example 1')
    test_cases = (
        [1], [1, 2], [1, 1, 2], [1, 20, 30, 40, 500, 500, 500],
        [5, 5, 5, 4, 4, 3, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        print(remove_duplicates(arr))
    print(arr)

    print('\n# count_sort example 1')
    test_cases = (
        [1, 2, 4, 3, 5], [5, 4, 3, 2, 1], [0, -5, -3, -4, -2, -1, 0],
        [-3, -2, -1, 0, 1, 2, 3], [1, 2, 3, 4, 3, 2, 1, 5, 5, 2, 3, 1],
        [10100, 10721, 10320, 10998], [-100320, -100450, -100999, -100001],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(f"Before: {arr}")
        result = count_sort(arr)
        print(f"After : {result}")

    print('\n# count_sort example 2')
    array_size = 5_000_000
    min_val = random.randint(-1_000_000_000, 1_000_000_000 - 998)
    max_val = min_val + 998
    case = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(case):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = count_sort(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# sorted_squares example 1')
    test_cases = (
        [1, 2, 3, 4, 5],
        [-5, -4, -3, -2, -1, 0],
        [-3, -2, -2, 0, 1, 2, 3],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(sorted(case)):
            arr[i] = value
        print(arr)
        result = sorted_squares(arr)
        print(result)

    print('\n# sorted_squares example 2')
    array_size = 5_000_000
    case = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(sorted(case)):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = sorted_squares(arr)
    print(f'Finished sorting large array of {array_size} elements')
