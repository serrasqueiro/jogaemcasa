#-*- coding: ISO-8859-1 -*-
#
# SLB dates at home!

import json
import datetime

# source: https://www.slbenfica.pt/pt-pt/jogos/calendario
# alt source: https://www.zerozero.pt/edition.php?id_edicao=165864
JOGOS_EM_CASA = (
    ["19-Aug-2023 20:30", "Estrela da Amadora"],
    ["02-Sep-2023 20:30", "Guimaraes"],
    ["01-Oct-2023", "FC Porto"],
    ["29-Oct-2023", "Casa Pia AC"],
    ["12-Nov-2023", "Sporting"],
    ["10-Dec-2023", "SC Farense"],
    ["29-Dec-2023", "FC Famalicao"],
    ["14-Jan-2024", "Rio Ave"],
    ["21-Jan-2024", "Boavista"],
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
        weekday = "?" if when is None else convert_to_pt_weekday(when.weekday())
        if weekday != "?":
            data = when.strftime("%a, %d %b %H:%M") if full else when.strftime("%a, %d %b (???)")
        else:
            data = "?"
        #print(data, what, "SLB vs", who)
        item = {
            "date": date,
            "weekday": weekday,
            "house": "SLB (Liga)" if what.startswith("L") else "SLB",
            "visitor": who,
        }
        res.append(item)
    json_string = json_dumper(res)
    #print(f"::: START\n{json_string}\n<<< END")
    dump_to(open("slb_dates.json", "w", encoding="ascii"), json_string)

def json_dumper(alist:list) -> str:
    a_str = json.dumps(alist, indent=2, sort_keys=True)
    return a_str

def dump_to(outfile, astr):
    outfile.write(astr)

def strptime(*args):
    if args[0] == "?":
        return None
    return datetime.datetime.strptime(*args)

def convert_to_pt_weekday(wday:int, lang="pt") -> str:
    if not lang:
        weekday = when.strftime("%A")
        return weekday
    days = ("2a.feira", "3a.feira", "4a.feira", "5a.feira", "6a.feira", "sabado", "domingo",)
    return days[wday]

if __name__ == "__main__":
    main()
