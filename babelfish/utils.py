#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals

from array import array


class DataTable(object):
    """A memory efficient strings data structure, loaded from a delimited text file."""
    def __init__(self, f, encoding='utf-8', delimiter='\t'):
        self.rows = 0
        self.columns = 0

        self._encoding = encoding

        self._data_array = array(b'b')
        self._pos_array = array(b'i')

        for l in f:
            e = l.decode(self._encoding).split(delimiter)
            self.columns = len(e)
            for u in e:
                b = len(self._data_array)
                self._data_array.fromstring(u.encode(self._encoding))
                self._pos_array.append(b)
            self.rows = self.rows + 1

    def get(self, row, column):
        """Retrieves an element from table"""
        start = self._pos_array[row * self.columns + column]
        end = self._pos_array[row * self.columns + column + 1]

        value_array = array(b'b')
        for i in xrange(start, end):
            value_array.append(self._data_array[i])

        return value_array.tostring().decode(self._encoding)

    def __len__(self):
        return self.rows
