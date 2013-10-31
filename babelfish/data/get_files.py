#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from __future__ import unicode_literals
import os.path
import tempfile
import zipfile
import requests


DATA_DIR = os.path.dirname(__file__)

# iso-3166-1.txt
with open(os.path.join(DATA_DIR, 'iso-3166-1.txt'), 'w') as f:
    r = requests.get('http://www.iso.org/iso/home/standards/country_codes/country_names_and_code_elements_txt.htm')
    f.write(r.content.strip())

# iso-639-3.tab
with tempfile.TemporaryFile() as f:
    r = requests.get('http://www-01.sil.org/iso639-3/iso-639-3_Code_Tables_20130531.zip')
    f.write(r.content)
    with zipfile.ZipFile(f) as z:
        z.extract('iso-639-3.tab', DATA_DIR)