# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import annotations

from babelfish.country import COUNTRY_MATRIX
from babelfish.exceptions import CountryConvertError, CountryReverseError

from . import CaseInsensitiveDict, CountryReverseConverter


class CountryNameConverter(CountryReverseConverter):
    codes: set[str]
    to_name: dict[str, str]
    from_name: CaseInsensitiveDict[str]

    def __init__(self) -> None:
        self.codes = set()
        self.to_name = {}
        self.from_name = CaseInsensitiveDict()
        for country in COUNTRY_MATRIX:
            self.codes.add(country.name)
            self.to_name[country.alpha2] = country.name
            self.from_name[country.name] = country.alpha2

    def convert(self, alpha2: str) -> str:
        if alpha2 not in self.to_name:
            raise CountryConvertError(alpha2)
        return self.to_name[alpha2]

    def reverse(self, code: str) -> str:
        if code not in self.from_name:
            raise CountryReverseError(code)
        return self.from_name[code]
