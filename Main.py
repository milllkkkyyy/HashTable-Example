
import random
from typing import TypeVar, List, Tuple

T = TypeVar("T")
Node = TypeVar("Node")
Table = TypeVar("Table")


class Node:
    __slots__ = ["key", "value", "deleted"]

    def __init__(self, key: str, value: T, deleted: bool = False) -> None:
        self.key = key
        self.value = value
        self.deleted = deleted

    def __str__(self) -> str:
        return f"Node({self.key}, {self.value})"

    __repr__ = __str__

    def __eq__(self, other: Node) -> bool:
        return self.key == other.key and self.value == other.value

    def __iadd__(self, other: T) -> None:
        self.value += other


class Table:
    """
    Hash Table
    """
    __slots__ = ['capacity', 'size', 'table', 'prime_index']

    primes = (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
        89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
        281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389,
        397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617,
        619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
        743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
        863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991,
        997)

    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

        i = 0
        while Table.primes[i] <= self.capacity:
            i += 1
        self.prime_index = i - 1

    def __eq__(self, other: Table) -> bool:
        """
        Equality operator
        :param other: other hash table we are comparing with this one
        :return: bool if equal or not
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False
        for i in range(self.capacity):
            if self.table[i] != other.table[i]:
                return False
        return True

    def __str__(self) -> str:
        """
        Represents the table as a string
        :return: string representation of the hash table
        """
        represent = ""
        bin_no = 0
        for item in self.table:
            represent += "[" + str(bin_no) + "]: " + str(item) + '\n'
            bin_no += 1
        return represent

    __repr__ = __str__

    def _hash_1(self, key: str) -> int:
        """
        Converts a string x into a bin number for the hash table
        :param key: key to be hashed
        :return: bin number to insert hash item at in our table, None if key is an empty string
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)
        return hashed_value % self.capacity

    def _hash_2(self, key: str) -> int:
        """
        Converts a string x into a hash
        :param key: key to be hashed
        :return: a hashed value
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)

        prime = Table.primes[self.prime_index]

        hashed_value = prime - (hashed_value % prime)
        if hashed_value % 2 == 0:
            hashed_value += 1
        return hashed_value
        
    def __len__(self) -> int:
        """
        amount of values in hash_table
        :param:
        :returns: int
        """
        return self.size

    def __setitem__(self, key: str, value: T) -> None:
        """
        sets the item in the hash_table
        :param: key: str, value: T
        :returns: None
        """
        self._insert(key, value)

    def __getitem__(self, key: str) -> T:
        """
        gets item in hash table
        :param: key: str
        :returns: T
        """
        node = self._get(key)
        if node is None:
            raise KeyError
        return node.value

    def __delitem__(self, key: str) -> None:
        """
        del items in hash table
        :param: key: str
        :returns: None
        """
        val = self._get(key)
        if val is None:
            raise KeyError('invalid key')
        else:
            self._delete(key)

    def __contains__(self, key: str) -> bool:
        """
        finds if hash_table has the value
        :param: key: str
        :returns: bool
        """
        val = self._get(key)
        if val is None:
            return False
        return True

    def _hash(self, key: str, inserting: bool = False) -> int:
        """
        gets_hash_index using either insert method or delete method
        :param: key:str, inserting: bool = False
        :returns: int
        """
        if inserting:
            i = 0
            index = self._hash_1(key) % self.capacity
            while self.table[index] is not None and not \
                    self.table[index].deleted and self.table[index].key != key:
                i += 1
                init_hash = self._hash_1(key)
                step_size = self._hash_2(key)
                index = (init_hash + i * step_size) % self.capacity
            return index
        else:
            i = 0
            index = self._hash_1(key) % self.capacity
            while self.table[index] is not None and self.table[index].key != key:
                i += 1
                init_hash = self._hash_1(key)
                step_size = self._hash_2(key)
                index = (init_hash + i * step_size) % self.capacity
            return index

    def _insert(self, key: str, value: T) -> None:
        """
        inserts index at given key, and value
        :param: key: str, value: T
        :returns: None
        """
        if key is None:
            return None
        hash_index = self._hash(key, True)
        self.table[hash_index] = Node(key, value)
        self.size += 1
        if self.size >= len(self.table) // 2:
            self._grow()

    def _get(self, key: str) -> Node:
        """
        gets hash_index
        :param: key: str
        :returns: Node
        """
        hash_index = self._hash(key)
        return self.table[hash_index]

    def _delete(self, key: str) -> None:
        """
        deletes keys
        :param: key: str
        :returns: None
        """
        hash_index = self._hash(key)
        self.table[hash_index].value = None
        self.table[hash_index].key = None
        self.table[hash_index].deleted = True
        self.size -= 1

    def _grow(self) -> None:
        """
        grows the table
        :param:
        :returns: None
        """
        old = self.table
        self.capacity = 2 * len(self.table)

        i = self.prime_index
        while Table.primes[i] <= self.capacity:
            i += 1
        self.prime_index = i - 1

        self.table = self.capacity * [None]

        i = 0
        self.size = 0
        while i < len(old):
            if old[i] is not None:
                if not old[i].deleted:
                    self._insert(old[i].key, old[i].value)
            i += 1

    def update(self, pairs: List[Tuple[str, T]] = []) -> None:
        """
        updates key with value, if the hey does not exist then inserts values
        :param: pairs: List[Tuple[str, T]] = []
        :returns: None
        """
        for key, val in pairs:
            in_dict = self._get(key)
            if in_dict:
                in_dict.value = val
            else:
                self._insert(key, val)

    def keys(self) -> List[str]:
        """
        returns keys of Nodes in table
        :param:
        :returns: List[str]
        """
        keys = []
        for item in self.table:
            if item is not None:
                keys.append(item.key)
        return keys

    def values(self) -> List[T]:
        """
        returns values of Nodes in table
        :param:
        :returns: List[T]
        """
        values = []
        for item in self.table:
            if item is not None:
                values.append(item.value)
        return values

    def items(self) -> List[Tuple[str, T]]:
        """
        returns tuple of keys, values in table
        :param:
        :returns: List:[Tuple[str, T]]
        """
        items = []
        for item in self.table:
            if item is not None:
                items.append((item.key, item.value))
        return items

    def clear(self) -> None:
        """
        empties the table
        :param:
        :return: None
        """
        self.table = self.capacity * [None]
        self.size = 0


class RequestHandler:
    """
    A request handler.
    """
    __slots__ = ["max_time", "data"]

    def __init__(self, max_time) -> None:
        """
        init the class
        :param: max_time
        :returns: None
        """
        self.max_time = max_time
        self.data = Table()

    def request(self, time: int, request_id: str, client_id: str) -> int:
        """
        handles the requests
        :param: time: int, request_id: str, client_id: str
        :returns: int
        """
        key = str(request_id + client_id)
        try:
            information = self.data[key]
            if information is not None:
                if time > information[1]:
                    self.data.update([(key, [0, time + self.max_time])])
                else:
                    self.data.update([(key, [information[0] + 1, time + self.max_time])])
            else:
                self.data[key] = [0, time + self.max_time]
        except KeyError:
            self.data[key] = [0, time + self.max_time]
        return self.data[key][0]
