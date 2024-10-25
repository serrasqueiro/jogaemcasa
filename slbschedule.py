#-*- coding: ISO-8859-1 -*-

""" slbschedule.py - Sport Lisboa e Benfica, calendario """

# source: https://www.slbenfica.pt/pt-pt/jogos/calendario
# alt source: https://www.zerozero.pt/competicao/liga-portuguesa?jornada_in=1&fase=198039
#
# Tabela classificativa:
#	https://www.zerozero.pt/edition.php?simp=0&id_edicao=187713

JOGOS_EM_CASA = (
    ["17-Aug-2024 20:30", "Casa Pia", 2],
    ["24-Aug-2024 20:30", "Estrela da Amadora"],
    ["30-Aug-2024 20:15", "Moreirense", 4, "Moreira de Conegos"],
    ["15-Sep-2024", "Santa Clara", 5],
    ["02-Oct-2024 20:00", "Atletico Madrid", "champions"],
    ["06-Oct-2024 18:00", "Nacional", 8, "Madeira"],
    ["19-Oct-2024 20:15", "Pevidem SC", "Tac,a de Portugal", "Guimaraes/ Selho"],
    ["23-Oct-2024 20:00", "Feyenoord", "champions"],
    ["27-Oct-2024 18:00", "Rio Ave", 9],
    ["30-Oct-2024 20:15", "Santa Clara", "Tac,a Liga"],
    ["02-Nov-2024 18:00", "Farense", 10, "Faro"],
    ["06-Nov-2024 20:00", "Bayern Munique", "champions", "Munique"],
    ["10-Nov-2024 20:45", "Porto", 11],
    ["23-Nov-2024 21:45", "Estrela Amadora", "Tac,a de Portugal"],
    ["27-Nov-2024 20:00", "Monaco", "champions", "Monaco"],
    ["01-Dec-2024 18:00", "FC Arouca", 12, "Arouca"],
)

TABELA = (
    """
P	J	V	E	D	GM	GS	DG		PC	JC	VC	EC	DC	GMC	GSC		PF	JF	VF	EF	DF	GMF	GSF	
1	Santa Clara	Santa Clara	3	1	1	0	0	4	1	+3		0	0	0	0	0	0	0		3	1	1	0	0	4	1	a
2	FC Porto	FC Porto	3	1	1	0	0	3	0	+3		3	1	1	0	0	3	0		0	0	0	0	0	0	0	a
3	Sporting	Sporting	3	1	1	0	0	3	1	+2		3	1	1	0	0	3	1		0	0	0	0	0	0	0	a
4	FC Famalicão	FC Famalicão	3	1	1	0	0	2	0	+2		3	1	1	0	0	2	0		0	0	0	0	0	0	0	a
5	Moreirense	Moreirense	3	1	1	0	0	2	1	+1		0	0	0	0	0	0	0		3	1	1	0	0	2	1	a
6	Vitória SC	Vitória SC	3	1	1	0	0	1	0	+1		0	0	0	0	0	0	0		3	1	1	0	0	1	0	a
7	Boavista	Boavista	3	1	1	0	0	1	0	+1		0	0	0	0	0	0	0		3	1	1	0	0	1	0	a
8	AVS	AVS	1	1	0	1	0	1	1	0		1	1	0	1	0	1	1		0	0	0	0	0	0	0	a
9	Est. Amadora	Est. Amadora	1	1	0	1	0	1	1	0		0	0	0	0	0	0	0		1	1	0	1	0	1	1	a
10	Nacional	Nacional	1	1	0	1	0	1	1	0		0	0	0	0	0	0	0		1	1	0	1	0	1	1	a
11	SC Braga	SC Braga	1	1	0	1	0	1	1	0		1	1	0	1	0	1	1		0	0	0	0	0	0	0	a
12	Farense	Farense	0	1	0	0	1	1	2	-1		0	1	0	0	1	1	2		0	0	0	0	0	0	0	a
13	Casa Pia AC	Casa Pia AC	0	1	0	0	1	0	1	-1		0	1	0	0	1	0	1		0	0	0	0	0	0	0	a
14	FC Arouca	FC Arouca	0	1	0	0	1	0	1	-1		0	1	0	0	1	0	1		0	0	0	0	0	0	0	a
15	Rio Ave	Rio Ave	0	1	0	0	1	1	3	-2		0	0	0	0	0	0	0		0	1	0	0	1	1	3	a
16	Benfica	Benfica	0	1	0	0	1	0	2	-2		0	0	0	0	0	0	0		0	1	0	0	1	0	2	a
17	Estoril Praia	Estoril Praia	0	1	0	0	1	1	4	-3		0	1	0	0	1	1	4		0	0	0	0	0	0	0	a
18	Gil Vicente	Gil Vicente	0	1	0	0	1	0	3	-3		0	0	0	0	0	0	0		0	1	0	0	1	0	3	a
"""
)

SIMPLE_NAMES = {
    "FC Porto": "Porto",
    "FC Famalicao": "Famalicao",
    "Vitoria SC": "Vitoria",
    "Est. Amadora": "Estrela da Amadora",
    "Casa Pia AC": "Casa Pia",
}

def sample(ascii_simpler, astr=None):
    res = []
    if astr is None:
        astr = TABELA
    tbl = [ala.split("\t") for ala in astr.lstrip().splitlines()]
    lens = sorted(set([len(ala) for ala in tbl]))
    assert 0 < len(lens) <= 2, "different lengths!"
    assert tbl[0][0] == "P", tbl[0][0]
    for line in tbl[1:]:
        #print(line[:3])
        assert line[1] == line[2], line[1]
        name = line[2]
        s_name = ascii_simpler(name)
        if s_name in SIMPLE_NAMES:
            s_name = SIMPLE_NAMES[s_name]
        res.append((0, s_name, name, line[3:]))
    return res, lens[-1] - 3
