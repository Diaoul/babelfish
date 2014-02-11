#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals

from array import array


class ArrayDataTable(object):
    """A full-memory strings data structure, loaded from a delimited text file."""
    def __init__(self, rows_iterable, encoding='utf-8', delimiter='\t'):
        self.rows = 0
        self.columns = 0
        self.encoding = encoding
        self.delimiter = delimiter
        self._data_array = array(b'b')
        self._pos_array = array(b'i')
        for row in rows_iterable:
            self._init_row(row)
            self.rows = self.rows + 1

    def _init_row(self, row):
        row_data = row.decode(self.encoding).split(self.delimiter)
        self.columns = len(row_data)
        for u in row_data:
            b = len(self._data_array)
            self._data_array.fromstring(u.encode(self.encoding))
            self._pos_array.append(b)

    def get(self, row, column):
        start = self._pos_array[row * self.columns + column]
        end = self._pos_array[row * self.columns + column + 1]

        value_array = array(b'b')
        for i in xrange(start, end):
            value_array.append(self._data_array[i])

        return value_array.tostring().decode(self.encoding)

    def __len__(self):
        return self.rows


class MmapDataTable(object):
    """A mmap-based strings data structure, loaded from a delimited text file."""
    def __init__(self, mmap_object, encoding='utf-8', delimiter='\t'):
        self._data_mmap = mmap_object
        self.encoding = encoding
        self.delimiter = delimiter
        self.rows = 0
        self.columns = 0
        self._pos_array = array(b'i')
        self._offset = self._data_mmap.tell()
        for row in iter(self._data_mmap.readline, b''):
            self._init_row(row)
            self.rows = self.rows + 1
            self._offset = self._data_mmap.tell()

    def _init_row(self, row):
        row_data = row.decode(self.encoding).split(self.delimiter)
        self.columns = len(row_data)
        pos = self._offset
        for u in row_data:
            self._pos_array.append(pos)
            pos = pos + len(u.encode(self.encoding)) + len(self.delimiter)

    def get(self, row, column):
        start = self._pos_array[row * self.columns + column]
        end = self._pos_array[row * self.columns + column + 1]

        data = self._data_mmap[start:end - 1]
        return data.decode(self.encoding)

    def __len__(self):
        return self.rows
