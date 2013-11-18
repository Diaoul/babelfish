# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from .alpha3b import Alpha3BConverter
from .alpha2 import Alpha2Converter
from ..exceptions import LanguageReverseError


class OpenSubtitlesConverter(Alpha3BConverter):
    def __init__(self):
        super(OpenSubtitlesConverter, self).__init__()
        self.codes |= { 'pob', 'pb', 'scc', 'mne' } # should we also add all the alpha2 codes?
        self.alpha2 = Alpha2Converter()
        self.to_opensubtitles = {('por', 'BR'): 'pob',
                                 ('gre', None): 'ell',
                                 ('srp', None): 'scc',
                                 ('srp', 'ME'): 'mne'}
        self.from_opensubtitles = {'pob': ('por', 'BR'),
                                   'pb': ('por', 'BR'),
                                   'ell': ('ell', None),
                                   'scc': ('srp', None),
                                   'mne': ('srp', 'ME')}

    def convert(self, alpha3, country=None, script=None):
        alpha3b = super(OpenSubtitlesConverter, self).convert(alpha3, country)
        if (alpha3b, country) in self.to_opensubtitles:
            return self.to_opensubtitles[(alpha3b, country)]
        return alpha3b

    def reverse(self, opensubtitles):
        if opensubtitles in self.from_opensubtitles:
            return self.from_opensubtitles[opensubtitles]
        try:
            return self.alpha2.reverse(opensubtitles)
        except LanguageReverseError:
            pass

        return super(OpenSubtitlesConverter, self).reverse(opensubtitles)
