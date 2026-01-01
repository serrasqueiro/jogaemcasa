""" mininorm.py -- Mini Normalizer of ASCII-7bit
"""

import unicodedata
from datetime import datetime, timezone


def ics_to_ymd(astr):
    return to_ymd_hhmm(parse_ics_datetime(astr))

def to_ymd_hhmm(dttm: datetime) -> str:
    return dttm.strftime("%Y-%m-%d %H:%M")

def parse_ics_datetime(astr:str) -> datetime:
    """ Value like "20260510T180000Z", parsed into date & time. """
    dttm = datetime.strptime(astr, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    return dttm


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
