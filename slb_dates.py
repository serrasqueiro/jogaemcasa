# SLB dates at home!

import json
import datetime

DATES = (
    ["07-Nov-2021 21:15", "Braga"],
    ["03-Dec-2021 21:15", "Sporting"],
    ["08-Dec-2021 20:00", "Kiev", "champions"],
    ["15-Dec-2021", "Covilha~", "tac,a"],
    ["19-Dec-2021", "Maritimo"],
    ["08-Jan-2022", "Moreirense"],
    ["30-Jan-2022", "Gil Vicente"],
    ["13-Feb-2022", "Santa Clara"],
    ["20-Mar-2022", "Estoril"],
    ["10-Apr-2022", "Belenenses"],
    ["24-Apr-2022", "Famalicao"],
    ["08-May-2022", "FC Porto"],	# los Porkos!
)

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
        weekday = when.weekday()
        data = when.strftime("%a, %d %b %H:%M") if full else when.strftime("%a, %d %b (???)")
        print(data, what, "SLB vs", who)
        item = {
            "date": date,
            "house": "SLB",
            "visitor": who,
        }
        if not what.startswith("L"):
            del item["house"]
        res.append(item)
    print(f"::: START\n{json_dumper(res)}\n<<< END")

def json_dumper(alist:list) -> str:
    a_str = json.dumps(alist, indent=2, sort_keys=True)
    return a_str

def strptime(*args):
    return datetime.datetime.strptime(*args)

if __name__ == "__main__":
    main()
