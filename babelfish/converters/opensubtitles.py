# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from .alpha3b import Alpha3BConverter


class OpenSubtitlesConverter(Alpha3BConverter):
    def __init__(self):
        super(OpenSubtitlesConverter, self).__init__()
        self.to_opensubtitles = {('por', 'BR'): 'pob'}
        self.from_opensubtitles = {'pob': ('por', 'BR')}

    def convert(self, alpha3, country=None):
        alpha3b = super(OpenSubtitlesConverter, self).convert(alpha3, country)
        if (alpha3b, country) in self.to_opensubtitles:
            return self.to_opensubtitles[(alpha3b, country)]
        return alpha3b

    def reverse(self, opensubtitles):
        if opensubtitles in self.from_opensubtitles:
            return self.from_opensubtitles[opensubtitles]
        return super(OpenSubtitlesConverter, self).reverse(opensubtitles)
