# Name:Alan Nortey
# OSU Email:noretya@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 2024-06-06
# Description: Hash Map implementation with Open Addressing


from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

    def hash_index(self, key: str, capacity: int, temp_buckets=None) -> int:
        """
        Helper function that calculates the hash index for a given key.
        If temp_buckets is provided, it returns the index of the first available bucket
        in temp_buckets. Otherwise, it returns the index in the current hash table.
        """
        if capacity is None:
            capacity = self._capacity

        index = self._hash_function(key) % capacity
        probe_index = 1
        initial_index = index

        if temp_buckets is not None:
            # Rehashing into a new table
            for _ in range(capacity):
                bucket = temp_buckets.get_at_index(index)
                if bucket is None or bucket.is_tombstone:
                    return index
                index = (initial_index + probe_index ** 2) % capacity
                probe_index += 1


        else:
            # Finding an index in the current table
            for _ in range(capacity):
                bucket = self._buckets.get_at_index(index)
                if bucket is None:
                    return index
                elif bucket.is_tombstone:
                    continue
                elif bucket.key == key:
                    return index

                index = (initial_index + probe_index ** 2) % capacity
                probe_index += 1



    def put(self, key: str, value: object) -> None:
        """
        Puts a key-value pair into a hash table
        """
        entry = HashEntry(key, value)
        # Check if load facter is 0.5 or bigger
        if self._size != 0:
            if self.table_load() >= 0.5:
                self.resize_table(self._capacity * 2)

        index = self.hash_index(key, self._capacity)
        bucket = self._buckets.get_at_index(index)
        # If bucket is not empty, then there is value at the index and index duplicate.
        if bucket:
            # Do nothing to bucket at index location if bucket is already filled
            bucket.value = value if bucket.key == key else bucket.value
            return
        self._buckets.set_at_index(index, entry)
        self._size += 1



    def resize_table(self, new_capacity: int) -> None:
        """
        Resize Hashtable capacity to a given value

        """
        if new_capacity < self.get_size():
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        self._size = 0
        self._capacity = new_capacity
        buckets = self._buckets
        self._buckets = DynamicArray()

        for i in range(new_capacity):
            self._buckets.append(None)

        for i in range(buckets.length()):
            entry = buckets.get_at_index(i)
            if entry:
                if buckets[i].is_tombstone is False:
                    self.put(entry.key, entry.value)


    def table_load(self) -> float:
        """
        Returns load factor of the current HashMap
        Load factor size divided by capacity
        """
        load_factor = self._size/self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets  in the hash table.
        """

        empty_counter = 0
        for index in range(self._capacity):
            if self._buckets[index] is None:
                empty_counter += 1
        return empty_counter


    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key.
         If the key is not in the hash the method returns None
        """
        index = self.hash_index(key, self.get_capacity())
        bucket = self._buckets[index]

        # Check if the bucket is not None and not a tombstone
        if bucket is not None and not bucket.is_tombstone:
            # If the key matches, return the value
            if bucket.key == key:
                return bucket.value

        # Perform quadratic probing until an empty bucket is found
        probe_index = 1
        initial_index = index
        while True:
            index = (initial_index + probe_index ** 2) % self._capacity
            bucket = self._buckets[index]

            # Check if the bucket is not None and not a tombstone
            if bucket is not None and not bucket.is_tombstone:
                # If the key matches, return the value
                if bucket.key == key:
                    return bucket.value

            # If we've probed all possible indices and haven't found the key, break the loop
            if index == initial_index:
                break

            probe_index += 1  # Increment the probe index for quadratic probing

        return None  # Return None if the key is not found



    def contains_key(self, key: str) -> bool:
        """
        Checks if the given key exists in the hash map.
        Returns True if the key is present, False otherwise.
        """

        # Calculate the hash index for the given key
        index = self._hash_function(key) % self._capacity

        # Retrieve the bucket at the calculated index
        bucket = self._buckets[index]

        # Check if the bucket is not None and is not a tombstone
        if bucket is not None and not bucket.is_tombstone:
            # If the bucket's key matches the given key, return True
            if bucket.key == key:
                return True

        # If the key is not found at the calculated index, perform quadratic probing
        probe_length = 1
        while True:
            # Calculate the next index using quadratic probing
            next_index = (index + probe_length ** 2) % self._capacity

            # Retrieve the bucket at the next index
            next_bucket = self._buckets[next_index]

            # Check if the next bucket is not None and is not a tombstone
            if next_bucket is not None and not next_bucket.is_tombstone:
                # If the next bucket's key matches the given key, return True
                if next_bucket.key == key:
                    return True

            # If we have checked all possible indices and haven't found the key, break the loop
            if next_index == index:
                break

            # Increment the probe length for quadratic probing
            probe_length += 1

        # If the key is not found after probing, return False
        return False

    def remove(self, key: str) -> None:
        """
        Method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing. Put a tombstone value at index where
        key was removed.
        """
        # Check if the key exists in the hash map.
        if not self.contains_key(key):
            return

            # Check if the hash map is empty.
        if self._buckets.length() < 1:
            return

            # Initialize variables for probe counting and hashing the key.
        probe_counter = 0
        hash_function = self._hash_function(key)

        # Loop until an empty slot is found.
        while True:
            # Calculate the index using quadratic probing.
            quad_probe_index = ((hash_function + (probe_counter * probe_counter)) % self.get_capacity())
            current_bucket = self._buckets.get_at_index(quad_probe_index)

            # If the key matches and the slot is not a tombstone, remove the entry.
            if key == current_bucket.key:
                if not current_bucket.is_tombstone:
                    current_bucket.is_tombstone = True
                    self._buckets.set_at_index(quad_probe_index, current_bucket)
                    self._size -= 1
                return

            # If the slot is empty or the probe exceeds the hash map size, exit the loop.
            if current_bucket is None or probe_counter >= self._buckets.length():
                return

            # Increment probe counter.
            probe_counter += 1





    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.
        """
        da = DynamicArray()

        for index in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(index)
            if bucket:
                if bucket.is_tombstone is False:
                    da.append((bucket.key, bucket.value))

        return da



    def clear(self) -> None:
        """Clear contents of Hash table"""
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def __iter__(self):
        """
        Iterator for hash map
        """
        # Initialize iterator index
        self._index = 0
        return self

    def __next__(self):
        """
        method will return the next item in the hash map, based on the current
        location of the iterator.
        """
        try:
            value = self._buckets[self._index]
            while value is None or value.is_tombstone is True:
                self._index += 1
                value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

            # Increment the index and return.

        self._index += 1
        return value


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)