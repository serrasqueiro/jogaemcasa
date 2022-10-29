#-*- coding: ISO-8859-1 -*-
#
# SLB dates at home!

import json
import datetime

# source: https://www.slbenfica.pt/pt-pt/jogos/calendario
# alt source: https://www.zerozero.pt/edition.php?id_edicao=165864
JOGOS_EM_CASA = (
    ["23-Aug-2022", "Dinamo Kiev", "champions"],
    ["30-Aug-2022 20:15", "Pac,os de Ferreira"],
    ["02-Sep-2022 18:00", "Vizela"],
    ["18-Sep-2022 18:00", "Maritimo"],
    ["05-Oct-2022 20:00", "PSG", "champions"],
    ["08-Oct-2022 18:00", "Rio Ave"],
    ["25-Oct-2022", "Juventus", "champions"],
    ["29-Oct-2022 18:00", "Chaves"],
    ["13-Nov-2022", "Gil Vicente"],
    ["26-Nov-2022 20:45", "Penafiel", "Tac,a Liga"],
    ["08-Jan-2023", "Portimonense"],
    ["15-Jan-2023", "Sporting"],
    ["05-Feb-2023", "Casa Pia"],
    ["19-Feb-2023", "Boavista"],
    ["05-Mar-2023", "Famalicao"],
    ["19-Mar-2023", "Vitoria FC"],
    ["08-Apr-2023", "FC Porto"],	# los porkos!
    ["23-Apr-2023", "Estoril"],
    ["07-May-2023", "Braga"],
    ["28-May-2023", "Santa Clara"],
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
