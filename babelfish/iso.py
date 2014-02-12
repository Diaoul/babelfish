#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals

from collections import namedtuple
from pkg_resources import resource_stream  # @UnresolvedImport

IsoCountry = namedtuple('IsoCountry', ['name', 'alpha2'])
IsoLanguage = namedtuple('IsoLanguage', ['alpha3', 'alpha3b', 'alpha3t', 'alpha2', 'scope', 'type', 'name', 'comment'])
IsoScript = namedtuple('IsoScript', ['code', 'number', 'name', 'french_name', 'pva', 'date'])


def get_countries_data():
    """Load countries ISO 3166-1 data"""
    f = resource_stream('babelfish', 'data/iso-3166-1.txt')
    f.readline()
    for l in f:
        iso_country = IsoCountry(*l.decode('utf-8').strip().split(';'))
        yield iso_country
    f.close()


def get_languages_data():
    """Load languages ISO 639-3 data"""
    f = resource_stream('babelfish', 'data/iso-639-3.tab')
    f.readline()
    for l in f:
        iso_language = IsoLanguage(*l.decode('utf-8').split('\t'))
        yield iso_language
    f.close()


def get_scripts_data():
    """Load scripts ISO 15924 data"""
    f = resource_stream('babelfish', 'data/iso15924-utf8-20131012.txt')
    f.readline()
    for l in f:
        l = l.decode('utf-8').strip()
        if not l or l.startswith('#'):
            continue
        script = IsoScript._make(l.split(';'))
        yield script
    f.close()
