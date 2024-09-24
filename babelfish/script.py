# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import annotations

from collections import namedtuple

from .compat import resource_stream

#: Script code to script name mapping
SCRIPTS = {}

#: List of countries in the ISO-15924 as namedtuple of code, number, name, french_name, pva and date
SCRIPT_MATRIX = []

#: The namedtuple used in the :data:`SCRIPT_MATRIX`
IsoScript = namedtuple('IsoScript', ['code', 'number', 'name', 'french_name', 'pva', 'date'])

with resource_stream('babelfish', 'data/iso15924-utf8-20131012.txt') as f:
    f.readline()
    for line in f:
        line = line.decode('utf-8').strip()
        if not line or line.startswith('#'):
            continue
        script = IsoScript._make(line.split(';'))
        SCRIPT_MATRIX.append(script)
        SCRIPTS[script.code] = script.name


class Script:
    """A human writing system.

    A script is represented by a 4-letter code from the ISO-15924 standard

    :param string script: 4-letter ISO-15924 script code

    """

    def __init__(self, script) -> None:
        if script not in SCRIPTS:
            msg = f'{script!r} is not a valid script'
            raise ValueError(msg)

        #: ISO-15924 4-letter script code
        self.code = script

    @property
    def name(self):
        """English name of the script."""
        return SCRIPTS[self.code]

    def __getstate__(self):
        return self.code

    def __setstate__(self, state):
        self.code = state

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.code == other
        if not isinstance(other, Script):
            return False
        return self.code == other.code

    def __ne__(self, other):
        return not self == other

    def __repr__(self) -> str:
        return f'<Script [{self}]>'

    def __str__(self) -> str:
        return self.code
