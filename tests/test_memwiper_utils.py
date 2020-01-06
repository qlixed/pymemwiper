import pytest
import memwiper.utils as mwutils

UNICODE_KIND = ["Wide Char", "1 Byte", "2 Byte", "4 Byte"]
UNICODE_WIDTH = {"1 Byte": 1, "2 Byte": 2, "4 Byte": 4}

# AFAIK the Wide Char is only used as representation on
# the C side of any Python/C API. So we don't test for it.
# Text on 1 Byte wide:
# s1 = "'Hello friend!' translated to spanish: '¡Hola amigo!'"
# Japanese text using 2 Byte wide unicode simbols
# s2 = "'Hello friend!' translated to japanese: 'こんにちは！'"
# Pi definition, uses 4 byte wide unicode simbols
# s3 = "Pi definition: 𝝅=𝑪/𝐝"


def test_memwiper_utils_kind(wideteststr):
    assert mwutils.kind(wideteststr) in UNICODE_KIND


def test_memwiper_utils_codepoints(wideteststr):
    assert mwutils.codepoints(wideteststr) == len(wideteststr)


def test_memwiper_utils_size(wideteststr):
    assert mwutils.size(wideteststr) in [
        len(wideteststr),
        len(wideteststr) * 2,
        len(wideteststr) * 4,
    ]


def test_memwiper_utils_funcs(wideteststr):
    kind = mwutils.kind(wideteststr)
    size = mwutils.size(wideteststr)
    codepoints = mwutils.codepoints(wideteststr)
    assert size == codepoints * UNICODE_WIDTH[kind]
