""" mininorm.py -- Mini Normalizer of ASCII-7bit
"""

import unicodedata

def to_ascii(text:str):
    """ Normalize accents, then drop anything above ASCII 127 """
    astr = ''.join(
        f"{discrete(c)}" for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return astr

def discrete(achr):
    one = ord(achr)
    if one < 127:
        return achr
    return f"(0x{one:04x}={unicodedata.category(achr)})"
