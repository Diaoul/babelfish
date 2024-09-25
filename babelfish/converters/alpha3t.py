# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import annotations

from typing import ClassVar

from babelfish.language import LANGUAGE_MATRIX

from . import LanguageEquivalenceConverter


class Alpha3TConverter(LanguageEquivalenceConverter):
    CASE_SENSITIVE: ClassVar[bool] = True
    SYMBOLS: ClassVar[dict[str, str]] = {}

    for iso_language in LANGUAGE_MATRIX:
        if iso_language.alpha3t:
            SYMBOLS[iso_language.alpha3] = iso_language.alpha3t
