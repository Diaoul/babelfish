# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from collections import namedtuple
from pkg_resources import resource_stream  # @UnresolvedImport
from . import basestr

#: Region code to region name mapping
REGIONS = {}

#: List of regions in the UN M.49 as namedtuple
REGION_MATRIX = []

#: The namedtuple used in the :data:`REGION_MATRIX`
UnRegion = namedtuple('UnRegion', ['global_code', 'global_name', 'region_code', 'region_name', 'sub_region_code',
                                   'sub_region_name', 'intermediate_region_code', 'intermediate_region_name',
                                   'country_area', 'm49_code', 'iso_alpha2', 'iso_alpha3', 'ldc', 'lldc', 'sids'])

with resource_stream('babelfish', 'data/un-m49.csv') as f:
    f.readline()
    for l in f:
        l = l.decode('utf-8').strip()
        if not l or l.startswith('#'):
            continue
        r = UnRegion._make(l.split(';'))
        REGION_MATRIX.append(r)
        if r.global_code not in REGIONS:
            REGIONS[r.global_code] = r.global_name
        if r.region_code not in REGIONS:
            REGIONS[r.region_code] = r.region_name
        if r.sub_region_code not in REGIONS:
            REGIONS[r.sub_region_code] = r.sub_region_name
        if r.intermediate_region_code not in REGIONS:
            REGIONS[r.intermediate_region_code] = r.intermediate_region_name
        REGIONS[r.m49_code] = r.country_area


class Region:
    """A human writing system

    A region is represented by a 3-letter numerical code from the UN M.49 standard

    :param string region: 3-letter UN M.49 numerical code

    """
    def __init__(self, region: str):
        if region not in REGIONS:
            raise ValueError(f'{region!r} is not a valid region')

        #: UN M.49 3-letter numerical code
        self.code = region

    @property
    def name(self):
        """English name of the region"""
        return REGIONS[self.code]

    def __getstate__(self):
        return self.code

    def __setstate__(self, state):
        self.code = state

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        if isinstance(other, basestr):
            return self.code == other
        if not isinstance(other, Region):
            return False
        return self.code == other.code

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return f'<Region [{self}]>'

    def __str__(self):
        return self.code
