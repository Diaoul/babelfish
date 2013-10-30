# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals


class Error(Exception):
    """Base class for all exceptions in babelfish"""
    pass


class ConvertError(Error):
    """Exception raised by converters when :meth:`~babelfish.converters.Converter.convert` fails

    :param string alpha3: alpha3 code that failed conversion
    :param country: country code that failed conversion, if any
    :type country: string or None

    """
    def __init__(self, alpha3, country):
        self.alpha3 = alpha3
        self.country = country

    def __str__(self):
        if self.country is None:
            return repr(self.alpha3)
        return repr(self.alpha3 + '-' + self.country)


class ReverseError(Error):
    """Exception raised by converters when :meth:`~babelfish.converters.ReverseConverter.reverse` fails

    :param string code: code that failed reverse conversion

    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)
