# -*- coding: utf-8 -*-


class TableEntry:
    def __init__(self):
        self.value = None
        self.depth = None
        self.flag = None


class TranspositionTable:
    _EXACT = 0
    _LOWERBOUND = 1
    _UPPERBOUND = 2

    def __init__(self):
        self._table = {}

    def get_table_entry(self, hash):
        return self._table.get(hash)

    def store(self, hash, table_entry):
        self._table[hash] = table_entry
