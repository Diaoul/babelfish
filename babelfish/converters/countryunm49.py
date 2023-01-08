# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from . import CountryReverseConverter, CaseInsensitiveDict
from ..exceptions import CountryConvertError, CountryReverseError
from ..region import REGION_MATRIX


class CountryUnM49Converter(CountryReverseConverter):
    def __init__(self):
        self.codes = set()
        self.to_code = {}
        self.from_code = CaseInsensitiveDict()
        for region in REGION_MATRIX:
            if region.iso_alpha2:
                self.codes.add(region.m49_code)
                self.to_code[region.iso_alpha2] = region.m49_code
                self.from_code[region.m49_code] = region.iso_alpha2

    def convert(self, alpha2):
        if alpha2 not in self.to_code:
            raise CountryConvertError(alpha2)
        return self.to_code[alpha2]

    def reverse(self, code):
        if code not in self.from_code:
            raise CountryReverseError(code)
        return self.from_code[code]
