"""
This module contains the Hash table data structure which
implements K MurmurHash3 hash functions, for existence check.
"""

from random import randint as random_number
from mmh3 import hash as murmurhash3


class HashTable:
    """
    Hash table data structure which implements K MurmurHash3 hash functions, for existence check.
    """
    def __init__(self, k, m):
        """
        Constructor for hash table which initialize the hash table.
        It construct the following properties:
        * Table consisting list of M zero values at first.
        * Randomized seed which is used for creating K different hash functions.
        * K different hash functions which is created by utility function `__initialize_hash_functions`

        :param k: Number of MurmurHash3 functions which the hash table will use.
        :param m: Size of the hash table elements.
        """
        self.__table = [0] * m
        self.__seed = random_number(1, 4096)
        self.__hash_functions = []
        self.__initialize_hash_functions(k)

    def __initialize_hash_functions(self, k):
        """
        Initialize K MurmurHash3 hash functions for the hash table.

        Each function will be different from each other, by using the multiplication of the randomized seed of
        the hash table with the index of the hash table.
        (under the assumption the K functions hashes in uniquely fashion)

        The MurmurHash3 functions then modulo by the table length, because the return value of
        the hash functions need to be in range [0, table length].

        :param k: Number of hash functions to initialize.
        """
        for index in range(1, k + 1):
            self.__hash_functions.append(
                lambda value: murmurhash3(value, self.__seed * index, False) % len(self.__table)
            )

    def insert(self, value):
        """
        Insert a given value into the hash table.
        For each of the hash functions, calculate the hashed key using given value
        and turn on the hashed key index in the internal table list.

        :param value: Value to insert into the hash table
        """

        # Value considered to be exists in the hash table if all the hashed keys returned
        # by all the hashed functions with the given value, are turned on.
        for index in range(len(self.__hash_functions)):
            hashed_key = self.__hash_functions[index](value)
            self.__table[hashed_key] = 1

    def check_existence(self, value):
        """
        Check existence of value in the hash table.
        The existence check determined by checking if all hash functions hashed keys are turned on
        in the internal table list.
        If all hashed keys turned on, the value is in the table, Otherwise it is not.

        :param value: Value to check if exists in the hash table.
        :return: True if the hash table contains the given value, Otherwise False.
        """

        # Checking for each of the hash functions, if one of them returning key
        # which is turned off -> means the value not in the internal table -> not in
        # the hash table.
        for index in range(len(self.__hash_functions)):
            if self.__table[self.__hash_functions[index](value)] == 0:
                return False
        return True
