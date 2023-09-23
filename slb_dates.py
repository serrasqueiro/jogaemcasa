#-*- coding: ISO-8859-1 -*-

""" SLB dates at home, and visiting! """

# pylint: disable=missing-function-docstring

import json
import datetime
from slbschedule import JOGOS_EM_CASA

LANG = "pt"

DATES = JOGOS_EM_CASA

VALID_WHAT = {
    "League": "Liga Portuguesa",
    "champions": "Champeons League",
    "europa": "Liga Europa",
    "Tac,a Liga": "Taça da Liga",
}

def main():
    res = []
    last = None
    for tup in DATES:
        item, _, when = item_from(tup)
        res.append(item)
        if last is not None:
            diff_days = difference_days(last, when)
            assert diff_days > 1, "difference too small"
        last = when
    json_string = json_dumper(res)
    #print(f"::: START\n{json_string}\n<<< END")
    dump_to(open("slb_dates.json", "w", encoding="ascii"), json_string)


def item_from(tup):
    what = "League"
    where = "(casa)"
    if len(tup) == 4:
        date, who, temp_what, where = tup
        if temp_what is not None:
            what = temp_what
    elif len(tup) == 3:
        date, who, what = tup
    else:
        date, who = tup
    full = False
    try:
        when = strptime(date, "%d-%b-%Y %H:%M")
        full = True
    except ValueError:
        when = strptime(date, "%d-%b-%Y")
    weekday = "?" if when is None else convert_to_weekday(when, LANG)
    if weekday == "?":
        data = "?"
    else:
        data = when.strftime("%a, %d %b %H:%M") if full else when.strftime("%a, %d %b (???)")
    is_liga = what in ("League",)
    if where == "(casa)":
        house_str = "SLB" + (" (Liga)" if is_liga else "")
        visitor_str = who
        print(data, what + "!", "SLB vs", who, "; what:", what, "; where:", where)
    else:
        house_str = who
        visitor_str = "SLB"
        print(data, what + "!", house_str, "vs", visitor_str, "; what:", what, "; where:", where)
    item = {
        "date": date,
        "weekday": weekday,
        "house": house_str,
        "visitor": visitor_str,
        "what": what.title(),
    }
    assert what in VALID_WHAT, data + "! " + what
    return item, data, when

def json_dumper(alist:list) -> str:
    a_str = json.dumps(alist, indent=2, sort_keys=True)
    return a_str + "\n"

def dump_to(outfile, astr):
    outfile.write(astr)

def strptime(*args):
    if args[0] == "?":
        return None
    return datetime.datetime.strptime(*args)

def convert_to_weekday(when=None, lang="pt") -> str:
    if when is None:
        when = datetime.datetime.now()
    wday_str = when.strftime("%A")
    if not lang:
        return wday_str
    days = ("2a.feira", "3a.feira", "4a.feira", "5a.feira", "6a.feira", "sabado", "domingo",)
    wday_str = days[when.weekday()]
    return wday_str

def difference_days(t0, t1):
    t_delta = t1 - t0
    #print("t1 - t0:", t1, t0, "; is:", t_delta.days)
    return t_delta.days

if __name__ == "__main__":
    main()
