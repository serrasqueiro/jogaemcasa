#-*- coding: ISO-8859-1 -*-
#
# SLB dates at home!

import json
import datetime

JOGOS_EM_CASA = (
    ["07-Nov-2021 21:15", "Braga"],
    ["03-Dec-2021 21:15", "Sporting"],
    ["08-Dec-2021 20:00", "Kiev", "champions"],
    ["15-Dec-2021", "Covilha~", "taça"],
    ["19-Dec-2021", "Maritimo"],
    ["08-Jan-2022", "Moreirense"],
    ["30-Jan-2022", "Gil Vicente"],
    ["13-Feb-2022", "Santa Clara"],
    ["20-Mar-2022", "Estoril"],
    ["10-Apr-2022", "Belenenses"],
    ["24-Apr-2022", "Famalicao"],
    ["08-May-2022", "FC Porto"],	# los Porkos!
)

DATES = JOGOS_EM_CASA

def main():
    res = list()
    for tup in DATES:
        what = "League"
        if len(tup) == 3:
            date, who, what = tup
        else:
            date, who = tup
        full = False
        try:
            when = strptime(date, "%d-%b-%Y %H:%M")
            full = True
        except ValueError:
            when = strptime(date, "%d-%b-%Y")
        weekday = convert_to_pt_weekday(when.weekday())
        data = when.strftime("%a, %d %b %H:%M") if full else when.strftime("%a, %d %b (???)")
        print(data, what, "SLB vs", who)
        item = {
            "date": date,
            "weekday": weekday,
            "house": "SLB (Liga)" if what.startswith("L") else "SLB",
            "visitor": who,
        }
        res.append(item)
    json_string = json_dumper(res)
    print(f"::: START\n{json_string}\n<<< END")
    dump_to(open("slb_dates.json", "w", encoding="ascii"), json_string)

def json_dumper(alist:list) -> str:
    a_str = json.dumps(alist, indent=2, sort_keys=True)
    return a_str

def dump_to(outfile, astr):
    outfile.write(astr)

def strptime(*args):
    return datetime.datetime.strptime(*args)

def convert_to_pt_weekday(wday:int, lang="pt") -> str:
    if not lang:
        weekday = when.strftime("%A")
        return weekday
    days = ("2a.feira", "3a.feira", "4a.feira", "5a.feira", "6a.feira", "sabado", "domingo",)
    return days[wday]

if __name__ == "__main__":
    main()
