import pytest
import memwiper


def make_str(the_char, length):
    if memwiper.utils.kind(the_char) == "1 Byte":
        scmp = "\U000000ff" * length
    if memwiper.utils.kind(the_char) == "2 Byte":
        scmp = "\U0000ffff" * length
    if memwiper.utils.kind(the_char) == "4 Byte":
        scmp = "\U000fffff" * length
    return scmp


def test_wipe(basicteststr):
    """
    Basic test of the wipe function
    """
    len_prewipe = len(basicteststr)
    memwiper.wipeit(basicteststr)
    assert len_prewipe == len(basicteststr)


def test_multiple_references(basicteststr):
    """
    Test with multiple references to the same string
    """
    s1 = basicteststr
    s2 = s1
    lenbasicteststr = len(basicteststr)
    memwiper.wipeit(s1)
    assert s1 == basicteststr
    assert len(s1) == lenbasicteststr
    assert s2 == basicteststr
    assert len(s2) == lenbasicteststr
    assert s1 == s2
    assert len(s1) == len(s2)


def test_widetest(widetestchar):
    print(widetestchar)


def test_long_string_wipe(widetestchar):
    """
    Test long (32k) string wipe
    """
    # Make s1 fixed side besides the len of s1
    s1 = widetestchar * int((2 ** 2) / len(widetestchar))
    len_prewipe = len(s1)
    memwiper.wipeit(s1)
    scmp = make_str(widetestchar, len_prewipe)
    assert type(s1) == type(scmp)
    assert len(s1) == len_prewipe
    assert s1 == scmp
    assert hash(s1) == hash(scmp)
    del s1


def test_huge_string_wipe(widetestchar):
    """
    Test HUGE (1M) string wipe
    """
    # Make s1 size 1M besides the len of s1
    s1 = widetestchar * int((2 ** 3) / len(widetestchar))
    len_prewipe = len(s1)
    memwiper.wipeit(s1)
    scmp = make_str(widetestchar, len_prewipe)
    assert type(s1) == type(scmp)
    assert len(s1) == len_prewipe
    assert s1 == scmp
    assert hash(s1) == hash(scmp)
    del s1
