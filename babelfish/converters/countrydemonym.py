# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from . import CountryReverseConverter, CaseInsensitiveDict
from ..country import DEMONYMS
from ..exceptions import CountryConvertError, CountryReverseError


class CountryDemonymConverter(CountryReverseConverter):
    def __init__(self):
        self.to_demonym = {}
        self.from_demonym = CaseInsensitiveDict()
        for alpha2, demonym in DEMONYMS.items():
            self.to_demonym[alpha2] = demonym
            self.from_demonym[demonym] = alpha2

    def convert(self, alpha2):
        if alpha2 not in self.to_demonym:
            raise CountryConvertError(alpha2)
        return self.to_demonym[alpha2]

    def reverse(self, demonym):
        if demonym not in self.from_demonym:
            raise CountryReverseError(demonym)
        return self.from_demonym[demonym]
