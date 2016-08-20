# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import re

from ._common import _validate_null_string
from ._error import InvalidCharError
from ._error import InvalidLengthError


__MAX_SHEET_NAME_LEN = 31

__INVALID_EXCEL_CHARS = "[]:*?/\\"

__RE_INVALID_EXCEL_SHEET_NAME = re.compile(
    "[{:s}]".format(re.escape(__INVALID_EXCEL_CHARS)))


def validate_excel_sheet_name(sheet_name):
    """
    :param str sheet_name: Excel sheet name to validate.
    :raises InvalidCharError:
        If the ``sheet_name`` is empty or includes invalid char(s):
        |invalid_excel_sheet_chars|.
    :raises InvalidLengthError:
        If the ``sheet_name`` is longer than 31 characters.
    """

    _validate_null_string(sheet_name)

    if len(sheet_name) > __MAX_SHEET_NAME_LEN:
        raise InvalidLengthError(
            "sheet name is too long: expected<={:d}, actual={:d}".format(
                __MAX_SHEET_NAME_LEN, len(sheet_name)))

    match = __RE_INVALID_EXCEL_SHEET_NAME.search(sheet_name)
    if match is not None:
        raise InvalidCharError(
            "invalid char found in the sheet name: '{:s}'".format(
                re.escape(match.group())))


def sanitize_excel_sheet_name(sheet_name, replacement_text=""):
    """
    Replace invalid characters for a Excel sheet name within the ``sheet_name``
    with the ``replacement_text``. Invalid characters are as follows:
    |invalid_excel_sheet_chars|.
    The ``sheet_name`` will truncated to 31 characters
    (max sheet name length of Excel) from the head, if the length
    of the name is exceed 31 characters.

    :param str sheet_name: Excel sheet name to sanitize.
    :param str replacement_text: Replacement text.
    :return: A replacement string.
    :rtype: str
    :raises ValueError: If the ``sheet_name`` is a invalid sheet name.
    """

    try:
        modify_sheet_name = __RE_INVALID_EXCEL_SHEET_NAME.sub(
            replacement_text, sheet_name.strip())
    except AttributeError as e:
        raise ValueError(e)

    return modify_sheet_name[:__MAX_SHEET_NAME_LEN]