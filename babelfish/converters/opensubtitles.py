# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from . import LanguageReverseConverter, CaseInsensitiveDict
from ..exceptions import LanguageReverseError


class OpenSubtitlesConverter(LanguageReverseConverter):
    def __init__(self):
        self.to_opensubtitles = {('por', 'BR'): 'pob', ('gre', None): 'ell', ('srp', None): 'scc', ('srp', 'ME'): 'mne'}
        self.from_opensubtitles = CaseInsensitiveDict({'pob': ('por', 'BR'), 'pb': ('por', 'BR'), 'ell': ('ell', None),
                                                       'scc': ('srp', None), 'mne': ('srp', 'ME')})

    @property
    def codes(self):
        from ..language import get_language_converter
        alpha3b_converter = get_language_converter('alpha3b')
        alpha2_converter = get_language_converter('alpha2')
        codes = (alpha2_converter.codes | alpha3b_converter.codes | set(['pob', 'pb', 'scc', 'mne']))
        return codes

    def convert(self, alpha3, country=None, script=None):
        from ..language import get_language_converter
        alpha3b_converter = get_language_converter('alpha3b')
        alpha3b = alpha3b_converter.convert(alpha3, country, script)
        if (alpha3b, country) in self.to_opensubtitles:
            return self.to_opensubtitles[(alpha3b, country)]
        return alpha3b

    def reverse(self, opensubtitles):
        from ..language import get_language_converter
        if opensubtitles in self.from_opensubtitles:
            return self.from_opensubtitles[opensubtitles]

        alpha3b_converter = get_language_converter('alpha3b')
        alpha2_converter = get_language_converter('alpha2')

        for conv in [alpha3b_converter, alpha2_converter]:
            try:
                return conv.reverse(opensubtitles)
            except LanguageReverseError:
                pass
        raise LanguageReverseError(opensubtitles)
