# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#


class Error(Exception):
    """Base class for all exceptions in babelfish"""
    pass


class NoConversionError(Error):
    """Raised when no conversion could be done with the
    converter on the given code

    """
    pass
