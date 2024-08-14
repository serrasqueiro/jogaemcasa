#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

""" SLB dates at home, and visiting! """

# pylint: disable=missing-function-docstring

import json
import datetime
import unidecode
import slbschedule

LANG = "pt"

DATES = slbschedule.JOGOS_EM_CASA

DUMP_TO_FILE = "slb_dates.json"	# Comment to not write to (any) json file!

VALID_WHAT = {
    "League": "Liga Portuguesa",
    "champions": "Champeons League",
    "europa": "Liga Europa",
    "Tac,a Liga": "Taça da Liga",
    "Tac,a de Portugal": "Taça de Portugal",
}

def main():
    dct = process_sample()
    run_script(dct)

def run_script(dct):
    assert dct, "No dictionary?"
    res = []
    last = None
    jorn = 0
    jorns = {}
    for tup in DATES:
        item, _, when, a_jorn, where = item_from(tup, dct)
        res.append(item)
        if last is not None:
            diff_days = difference_days(last, when)
            assert diff_days >= 0, f"must be increasing: {tup}"
            assert diff_days > 1, f"difference too small: {last} then {when}"
        last = when
        if item["what"] == "League":
            if a_jorn > 0:
                jorn = a_jorn
            elif jorn > 0:
                jorn += 1
            if jorn > 0:
                assert jorn not in jorns, f"Jornada {jorn} repetida ?!"
                jorns[jorn] = (item, where)
    json_string = json_dumper(res)
    #print(f"::: START\n{json_string}\n<<< END")
    if "DUMP_TO_FILE" in globals() and DUMP_TO_FILE:
        dump_to(open(DUMP_TO_FILE, "w", encoding="ascii"), json_string)
    print("--" * 20)
    dump_league(jorns)
    return res, jorns

def dump_league(jorns, verbose=0):
    checks = {
        "C": [],
        "F": [],
    }
    num_jorn = 34
    for jorn in range(1, num_jorn + 1):
        if jorn not in jorns:
            print(f'Jornada {jorn:>3}: ---')
            continue
        key = jorn
        item, where = jorns[key]
        weekday = item["weekday"]
        is_home = where == "(casa)"
        if is_home:
            rest = "***** casa *****"
            checks["C"].append(item["visitor"])
        else:
            rest = where
            checks["F"].append(item["house"])
        rest = "  " + rest
        fight = f'{item["house"]} - {item["visitor"]}'
        fight = fight.replace("SLB (Liga)", "Benfica")
        if verbose > 0:
            pre = f"(Ronda {int(jorn > (num_jorn // 2))+1}) "
            pre += "C" if "*****" in rest else "F"
            pre = " " + pre
        else:
            pre = ""
        print(f'Jornada {key:>3}{pre}:  {weekday:<.3} {item["date"]:<20} {fight:<28}{rest}')
    if verbose <= 0:
        return True
    print(checks["C"])
    print(checks["F"])
    return True

def item_from(alist, dct, debug=0):
    mydict = {} if dct is None else dct
    tup = alist
    jorn = 0
    what = "League"
    where = "(casa)"
    if len(tup) >= 3:
        if isinstance(tup[2], int):
            jorn = tup[2]
            tup[2] = "League"
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
        x_home = "Benfica"
        x_visitor = who
        house_str = "SLB" + (" (Liga)" if is_liga else "")
        visitor_str = who
        print(data, what + "!", "SLB vs", who, "; what:", what, "; where:", where)
    else:
        house_str = who
        x_home = house_str
        x_visitor = "Benfica"
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
    if is_liga:
        if debug > 0:
            print("Debug:", alist)
        assert x_home in dct, f"x_home? {x_home}"
        assert x_visitor in dct, f"x_visitor? {x_visitor}"
    return item, data, when, jorn, where

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

def process_sample():
    """ Returns the dictionary of club names. """
    dct = {}
    tup = slbschedule.sample(unidecode.unidecode)
    news, _ = tup
    for quad in news:
        _, s_name, name, line = quad
        #print(s_name, line)
        dct[s_name] = name
    return dct

if __name__ == "__main__":
    main()
