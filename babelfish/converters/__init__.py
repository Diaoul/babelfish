# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#


class Converter(object):
    """A :class:`Converter` supports converting an alpha3 language code with an
    alpha2 country code and a script code into a custom code

    .. attribute:: codes

        Set of possible custom codes

    """
    def convert(self, alpha3, country=None, script=None):
        """Convert an alpha3 language code with an alpha2 country code and a script code
        into a custom code

        :param string alpha3: ISO-639-3 language code
        :param country: ISO-3166 country code, if any
        :type country: string or None
        :param script: ISO-15924 script code, if any
        :type script: string or None
        :return: the corresponding custom code
        :rtype: string
        :raise: :class:`~babelfish.exceptions.ConvertError`

        """
        raise NotImplementedError


class ReverseConverter(Converter):
    """A :class:`Converter` able to reverse a custom code into a alpha3
    ISO-639-3 language code, alpha2 ISO-3166-1 country code and ISO-15924 script code

    """
    def reverse(self, code):
        """Reverse a custom code into alpha3, country and script code

        :param string code: custom code to reverse
        :return: the corresponding alpha3 ISO-639-3 language code, alpha2 ISO-3166-1 country code and ISO-15924 script code
        :rtype: tuple
        :raise: :class:`~babelfish.exceptions.ReverseError`

        """
        raise NotImplementedError
