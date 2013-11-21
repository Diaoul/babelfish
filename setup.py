#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#
from setuptools import setup, find_packages


setup(name='babelfish',
    version='0.4.0',
    license='BSD',
    description='A module to work with countries and languages',
    long_description=open('README.rst').read() + '\n\n' + open('HISTORY.rst').read(),
    keywords='babelfish language country locale',
    url='https://github.com/Diaoul/babelfish',
    author='Antoine Bertin',
    author_email='diaoulael@gmail.com',
    packages=find_packages(),
    package_data={'babelfish': ['data/iso-639-3.tab', 'data/iso-3166-1.txt', 'data/iso15924-utf8-20131012.txt',
                                'data/opensubtitles_languages.txt']},
    classifiers=['Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Multimedia :: Video',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    test_suite='babelfish.tests.suite',
    entry_points={'babelfish.language_converters': ['alpha2 = babelfish.converters.alpha2:Alpha2Converter',
                                                    'alpha3b = babelfish.converters.alpha3b:Alpha3BConverter',
                                                    'alpha3t = babelfish.converters.alpha3t:Alpha3TConverter',
                                                    'name = babelfish.converters.name:NameConverter',
                                                    'scope = babelfish.converters.scope:ScopeConverter',
                                                    'type = babelfish.converters.type:LanguageTypeConverter',
                                                    'opensubtitles = babelfish.converters.opensubtitles:OpenSubtitlesConverter'],
                  'babelfish.country_converters': ['name = babelfish.converters.countryname:CountryNameConverter']
    })
