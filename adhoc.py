#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

""" SLB dates at home, and visiting! """

# pylint: disable=missing-function-docstring

import os.path

FILE = os.path.join(os.path.dirname(__file__), "adhoc.csv")



def main():
    do_script(FILE)

def do_script(csv_in):
    dprint("# Using:", csv_in, force=True)
    with open(csv_in, "r", encoding="ascii") as fdin:
        lines = [
            (idx, aba.rstrip())
            for idx, aba in enumerate(fdin.readlines(), 1)
            if aba and not aba.startswith("#")
        ]
    for tup in lines:
        dprint(":::", tup)


def dprint(*args, **kwargs):
    do_show = kwargs.pop("force", False)
    if not do_show:
        return False
    print(*args, **kwargs)
    return True


if __name__ == "__main__":
    main()
