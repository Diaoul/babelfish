# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from . import LanguageReverseConverter
from .alpha3b import Alpha3BConverter
from .alpha2 import Alpha2Converter
from ..exceptions import LanguageReverseError


class OpenSubtitlesConverter(LanguageReverseConverter):
    def __init__(self):
        self.alpha3b_converter = Alpha3BConverter()
        self.alpha2_converter = Alpha2Converter()

        self.codes = (self.alpha2_converter.codes |
                      self.alpha3b_converter.codes |
                      { 'pob', 'pb', 'scc', 'mne' })

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
        alpha3b = self.alpha3b_converter.convert(alpha3, country, script)
        if (alpha3b, country) in self.to_opensubtitles:
            return self.to_opensubtitles[(alpha3b, country)]
        return alpha3b

    def reverse(self, opensubtitles):
        opensubtitles = opensubtitles.lower()

        try:
            return self.from_opensubtitles[opensubtitles]
        except KeyError:
            pass

        for conv in [self.alpha3b_converter, self.alpha2_converter]:
            try:
                return conv.reverse(opensubtitles)
            except LanguageReverseError:
                pass

        raise LanguageReverseError(opensubtitles)
