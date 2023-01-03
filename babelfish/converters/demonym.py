# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
from . import LanguageReverseConverter
from .. import CountryReverseError, Language
from ..country import country_converters
from ..language import language_converters


class DemonymConverter(LanguageReverseConverter):
    def __init__(self):
        self.demonym_converter = country_converters['demonym']
        self.name_converter = language_converters['name']

    def convert(self, alpha3, country=None, script=None):
        name = self.name_converter.convert(alpha3)
        if country is None:
            return name

        demonym = self.demonym_converter.convert(country)
        return f'{demonym} {name}'

    def reverse(self, demonym):
        values = demonym.split(' ')
        for i in range(len(values) - 1, 0, -1):
            try:
                country = self.demonym_converter.reverse(' '.join(values[0:i]))
            except CountryReverseError:
                continue

            alpha3 = self.name_converter.reverse(values[i])[0]
            return alpha3, country, None

        return self.name_converter.reverse(demonym)
