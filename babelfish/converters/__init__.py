# Copyright (c) 2013 the BabelFish authors. All rights reserved.
# Use of this source code is governed by the 3-clause BSD license
# that can be found in the LICENSE file.
#


class Converter(object):
    """A :class:`Converter` supports converting an alpha3 language code with an
    alpha2 country code into a custom code

    """
    def convert(self, alpha3, country=None):
        """Convert an alpha3 language code with an alpha2 country code
        into a custom code

        :param string alpha3: ISO-639-3 language code
        :param country: ISO-3166 country code, if any
        :type country: string or None
        :return: the corresponding custom code
        :rtype: string

        """
        raise NotImplementedError


class ReverseConverter(Converter):
    """A :class:`Converter` able to reverse a custom code into a alpha3
    ISO-639-3 language code and alpha2 ISO-3166-1 country code

    """
    def reverse(self, code):
        """Reverse a custom code into alpha3 and country code

        :param string code: custom code to reverse
        :return: the corresponding alpha3 ISO-639-3 language code and alpha2 ISO-3166-1 country code
        :rtype: tuple

        """
        raise NotImplementedError
