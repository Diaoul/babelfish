# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import annotations

from typing import ClassVar

from babelfish.exceptions import LanguageConvertError
from babelfish.language import LANGUAGE_MATRIX

from . import LanguageConverter


class LanguageTypeConverter(LanguageConverter):
    FULLNAME: ClassVar[dict[str, str]] = {
        'A': 'ancient',
        'C': 'constructed',
        'E': 'extinct',
        'H': 'historical',
        'L': 'living',
        'S': 'special',
    }
    SYMBOLS: ClassVar[dict[str, str]] = {}
    for iso_language in LANGUAGE_MATRIX:
        SYMBOLS[iso_language.alpha3] = iso_language.type
    codes: ClassVar[set[str]] = set(SYMBOLS.values())

    def convert(self, alpha3: str, country: str | None = None, script: str | None = None) -> str:
        if self.SYMBOLS[alpha3] in self.FULLNAME:
            return self.FULLNAME[self.SYMBOLS[alpha3]]
        raise LanguageConvertError(alpha3, country, script)
