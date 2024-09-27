# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass

from .compat import resource_stream

#: The namedtuple used in the :data:`SCRIPT_MATRIX`
IsoScript = namedtuple('IsoScript', ['code', 'number', 'name', 'french_name', 'pva', 'date'])

#: Script code to script name mapping
SCRIPTS: dict[str, str] = {}

#: List of scripts in the ISO-15924 as namedtuple of code, number, name, french_name, pva and date
SCRIPT_MATRIX: list[IsoScript] = []


with resource_stream('babelfish', 'data/iso15924-utf8-20131012.txt') as f:
    f.readline()
    for raw_line in f:
        line = raw_line.decode('utf-8').strip()
        if not line or line.startswith('#'):
            continue
        script = IsoScript._make(line.split(';'))
        SCRIPT_MATRIX.append(script)
        SCRIPTS[script.code] = script.name


@dataclass(frozen=True)
class Script:
    """A human writing system.

    A script is represented by a 4-letter code from the ISO-15924 standard

    :param string script: 4-letter ISO-15924 script code

    """

    #: ISO-15924 4-letter script code
    script: str

    def __post_init__(self) -> None:
        if self.script not in SCRIPTS:
            msg = f'{self.script!r} is not a valid script'
            raise ValueError(msg)

    @property
    def code(self) -> str:
        return self.script

    @property
    def name(self) -> str:
        """English name of the script."""
        return SCRIPTS[self.code]

    def __repr__(self) -> str:
        return f'<Script [{self}]>'

    def __str__(self) -> str:
        return self.code
