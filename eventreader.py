#-*- coding: UTF-8 -*-

""" Event reader """

import json
import mininorm


def main():
    """ Debug:
	import importlib; import eventreader; importlib.reload(eventreader)
    """
    with open("SL_Benfica.ics", "r", encoding="utf-8") as fdin:
        text = fdin.read()
    evt = ICSParser(text)
    with open("my.json", "w", encoding="ascii") as fdout:
        fdout.write(evt.json_it())
    return evt


class ICSParser:
    """ ics file parser """
    def __init__(self, text):
        self.text = text
        self.events = []
        self._seq = self._parse()

    def sequence(self):
        return self._seq

    def my_events(self):
        """ Return events sorted by start datetime, yielding only the first 3 fields."""
        events_sorted = sorted(
            self._seq,
            key=lambda e: e[1][0],
        )
        return (
            {
                "index": aba[0],
                "date": aba[1][0],
                "desc": aba[2],
            }
            for aba in events_sorted
        )

    def json_it(self):
        """ Use 'with open("my.json", "w", encoding="ascii") as fdout: fdout.write(...)' """
        mine = list(self.my_events())
        astr = json.dumps(mine, indent=2, sort_keys=True, ensure_ascii=True)
        return astr + "\n"

    def _parse(self):
        """Parse the ICS text into VEVENT dictionaries."""
        blocks = self._extract_blocks()
        evt = [
            self._parse_block(b) for b in blocks
        ]
        self.events = evt
        lst = [
            (
                num,
                (aba["DTSTART-HM"], aba["DTEND-HM"]),
                aba["SUM-7BIT"],
                sorted(aba),
                len(aba["@ignore"]),
            )
            for num, aba in enumerate(evt, 1)
        ]
        return lst

    def _extract_blocks(self):
        """Return raw VEVENT blocks as strings."""
        blocks = []
        current = None
        for raw in self.text.splitlines():
            line = raw.strip()
            if line == "BEGIN:VEVENT":
                current = []
                continue
            if line == "END:VEVENT":
                if current is not None:
                    blocks.append("\n".join(current))
                    current = None
                continue
            if current is not None:
                current.append(line)
        return blocks

    def _parse_block(self, block):
        """Convert a VEVENT block into a dict of key/value pairs."""
        event = {
            "@ignore": [],
        }
        for num, line in enumerate(block.splitlines(), 1):
            if ":" not in line:
                event["@ignore"].append((num, line))
                continue
            s_key, value = line.split(":", 1)
            key = to_ascii7(s_key.replace("\\n", "+"), "s_key")
            event[key] = value
            if key in ("SUMMARY",):
                event["SUM-7BIT"] = to_ascii7(value, "7BIT")
            elif key in ("DTSTART", "DTEND"):
                event[key + "-HM"] = nice_date(value)
        return event

    def __iter__(self):
        """Allow iteration over events."""
        return iter(self.events)

    def __len__(self):
        return len(self.events)


def to_ascii7(astr, context=""):
    """ Simpler ASCII, convert accented letters into normal 7bit ASCII. """
    assert isinstance(astr, str), context
    spl = astr.splitlines()
    these = [
        mininorm.to_ascii(line) for line in spl
    ]
    astr = '\n'.join(these)
    if len(these) > 1:
        return astr + '\n'
    return astr

def nice_date(astr):
    return mininorm.ics_to_ymd(astr)


if __name__ == "__main__":
    main()
