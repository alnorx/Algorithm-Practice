# Name:Alan Nortey
# OSU Email:noretya@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 2024-06-06
# Description: Hash Map implementation with separate chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Put new key and value in to hash table
        """

        load_factor = self.get_size() / self.get_capacity()
        if load_factor >= 1.0:
            self.resize_table(self.get_capacity() * 2)

        index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets[index]

        node = bucket.contains(key)
        if node:
            node.value = value
        else:
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize array to the given capacity
        """
        if new_capacity < 1:
            return

            # Initialize a new linked list to store key-value pairs temporarily
        linked_list_temp = LinkedList()

        # Initialize a new dynamic array to hold the resized buckets
        dynamic_array_new = DynamicArray()

        # If the new capacity is not a prime number, adjust it to the next prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Populate the dynamic array with new linked lists
        for _ in range(new_capacity):
            dynamic_array_new.append(LinkedList())

        # Copy entries and insert them to new hash table
        # Add key-value pairs into the new buckets.
        for bucket_index in range(self.get_capacity()):
            node_to_add = self._buckets.get_at_index(bucket_index)
            if node_to_add is not None:
                for node in node_to_add:
                    linked_list_temp.insert(node.key, node.value)


        # Update the hash table attributes
        self._size = 0
        self._buckets = dynamic_array_new
        self._capacity = new_capacity

        for node in linked_list_temp:
            self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        Returns load factor of the current HashMap
        Load factor size divided by capacity
        """
        load_factor = self._size/self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        empty_counter = 0
        for index in range(self._capacity):
            # Find linked list for for each bucket
            bucket_linked_list = self._buckets[index]
            # If linked list length is zero bucket is empty.
            if bucket_linked_list.length() == 0:
                empty_counter += 1
        return empty_counter





    def get(self, key: str) -> object:
        """
        Returns value associated with a given key.
        If the key is not in the hashmap returns None
        """
        index = self._hash_function(key) % self._capacity
        bucket_linked_list = self._buckets[index]
        node = bucket_linked_list.contains(key)

        if node is None:
            return None
        else:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map.
        If key is not present, it returns False. An
        empty hash map does not contain any keys
        """

        if self._size == 0:
            return False
        index = self._hash_function(key) % self._capacity
        bucket_linked_list = self._buckets[index]
        if bucket_linked_list.contains(key):
            return True
        return False



    def remove(self, key: str) -> None:
        """
        Method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing
        """
        if not self.contains_key(key):
            return

        index = self._hash_function(key) % self._capacity
        bucket_linked_list = self._buckets[index]

        # Use LinkedList remove method to remove key
        if bucket_linked_list.remove(key):
            self._size -= 1



    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.
        """
        da = DynamicArray()


        for i in range(self._buckets.length()):
            # Check if the bucket contains any nodes
            if self._buckets[i].length() > 0:
                # Iterate through the nodes in the linked list
                for node in self._buckets[i]:
                    # Append the key-value pair to the dynamic array
                    da.append((node.key, node.value))

        return da


    def clear(self) -> None:
        """
        This method clears the contents of the hash map. The hash
        table capacity is not altered
        """
        for index in range(self._capacity):
            # Set bucket linked list at each index to an empty  list
            self._buckets[index] = LinkedList()
        self._size = 0




def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Take Dynamic array as an argument and returns the most
    occurring entry and the frequency of the entries
    """


   # Create a HashMap to store the frequency of each element
    frequency_map = HashMap()

    # Populate the HashMap with the frequencies of each element
    for i in range(da.length()):
        key = da[i]
        if frequency_map.contains_key(key):
            frequency_map.put(key, frequency_map.get(key) + 1)
        else:
            frequency_map.put(key, 1)

    # Find the highest frequency and collect all elements with that frequency
    max_frequency = 0
    modes = DynamicArray()

    for bucket_index in range(frequency_map._capacity):
        bucket = frequency_map._buckets[bucket_index]
        node = bucket._head
        while node:
            frequency = node.value
            if frequency > max_frequency:
                max_frequency = frequency
                # Reset modes to only include current highest frequency element
                modes = DynamicArray()
                modes.append(node.key)
            elif frequency == max_frequency:
                modes.append(node.key)
            node = node.next

    return modes, max_frequency
# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
