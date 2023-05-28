#-*- coding: ISO-8859-1 -*-
#
# SLB titles !

""" Dumps text for SLB titles !
"""

# pylint: disable=missing-function-docstring

from unidecode import unidecode

TITLES = {
    1935: "L",	# Lippo Hertzka
    1936: "L",
    1937: "L",
    1941: "J",	# Janos Biri
    1942: "J",
    1944: "J",
    1949: "TS",	# Ted Smith
    1954: "O",	# Otto Glória
    1956: "O",
    1959: "B",	# Béla Guttmann
    1960: "B",
    1962: "F",	# Fernando Riera
    1963: "LC",	# Lajos Czeizer
    1964: "ES",
    1966: "F",
    1967: "O",
    1968: "O",
    1970: "JH",
    1971: "JH",
    1972: "JH",
    1974: "MP",
    1975: "MW",
    1976: "JM",
    1980: "LB",
    1982: "E",
    1983: "E",
    1986: "JM",
    1988: "T",
    1990: "E",
    1993: "T",
    2004: "TR",
    2009: "JJ",
    2013: "JJ",
    2014: "JJ",
    2015: "RV",
    2016: "RV",
    2018: "BL",
    2022: "RS",
}

TRAINER_TO_NAME = {
    "B": "Béla Guttman",
    "BL": "Bruno Lage",
    "E": "Eriksson",
    "ES": "Elek Schwartz",
    "F": "Fernando Riera",
    "J": "Janos Biri",
    "JJ": "Jorge Jesus",
    "JH": "Jimmy Hagan",
    "JM": "John Mortimore",
    "L": "Lippo Hertzka",
    "LB": "Lajos Baroti",
    "LC": "Lajos Czeizer",
    "MP": "Milorad Pavic",
    "MW": "Mario Wilson",
    "O": "Otto Gloria",
    "RS": "Roger Smith",
    "RV": "Rui Vitoria",
    "T": "Toni",
    "TR": "Trapattoni",
    "TS": "Ted Smith",
    "z": "***nada***",
}


def main():
    alist = show_names(TRAINER_TO_NAME, False)
    if __file__.endswith("slb_trainers.py"):
        print('\n'.join(alist))
        print("++" * 20)
    dump_titles(TITLES)

def dump_titles(title_dct):
    for idx, key in enumerate(sorted(title_dct), 1):
        abbrev = title_dct.get(key)
        num = key % 100
        name = TRAINER_TO_NAME.get(abbrev)
        post = name if name else abbrev
        print(f"#{idx:<3} {key}/{num+1:02} {post}")

def show_names(dct:dict, dump=True):
    """ Shows and returns string list of abbreviation + name,
    separated by blanks.
    """
    res = []
    names = {}
    in_use = {}
    for key, name in dct.items():
        names[name] = key
    for num, abbrev in TITLES.items():
        assert num > 1900, "Invalid year"
        assert abbrev in dct, f"year={num}, abbrev={abbrev}"
        in_use[abbrev] = num
    for name in sorted(names, key=str.casefold):
        abbrev = names[name]
        astr = f"{abbrev:.<5} {shown_name(name)}"
        res.append(astr)
        assert abbrev == "z" or abbrev in in_use, astr
    if not dump:
        return res
    for astr in res:
        print(astr)
    return res

def shown_name(astr):
    """ Returns normalized name, without accents: ascii only! """
    return unidecode(astr)

if __name__ == "__main__":
    main()
