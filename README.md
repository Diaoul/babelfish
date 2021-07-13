# BabelFish
BabelFish is a Python library to work with countries and languages.

[![tests](https://github.com/Diaoul/babelfish/actions/workflows/test.yml/badge.svg)](https://github.com/Diaoul/babelfish/actions/workflows/test.yml)

## Usage
BabelFish provides scripts, countries and languages from their respective ISO
standards and a handy way to manipulate them with converters.

### Script
Script representation from 4-letter code (ISO-15924):
```python
>>> import babelfish
>>> script = babelfish.Script('Hira')
>>> script
<Script [Hira]>
```

### Country
Country representation from 2-letter code (ISO-3166):
```python
>>> country = babelfish.Country('GB')
>>> country
<Country [GB]>
```

Built-in country converters (name):
```python
>>> country = babelfish.Country('GB')
>>> country
<Country [GB]>
```

### Language
Language representation from 3-letter code (ISO-639-3):
```python
>>> language = babelfish.Language("eng")
>>> language
<Language [en]>
```

Country-specific language:
```python
>>> language = babelfish.Language('por', 'BR')
>>> language
<Language [pt-BR]>
```

Language with specific script:
```python
>>> language = babelfish.Language.fromalpha2('sr')
>>> language.script = babelfish.Script('Cyrl')
>>> language
<Language [sr-Cyrl]>
```

Built-in language converters (alpha2, alpha3b, alpha3t, name, scope, type and opensubtitles):
```python
>>> language = babelfish.Language('por', 'BR')
>>> language.alpha2
'pt'
>>> language.scope
'individual'
>>> language.type
'living'
>>> language.opensubtitles
'pob'
>>> babelfish.Language.fromalpha3b('fre')
<Language [fr]>
```

## License
BabelFish is licensed under the [3-clause BSD license](http://opensource.org/licenses/BSD-3-Clause>)

Copyright (c) 2013, the BabelFish authors and contributors.
