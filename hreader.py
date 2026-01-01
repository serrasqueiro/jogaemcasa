#-*- coding: ISO-8859-1 -*-

""" HTML reader """

from bs4 import BeautifulSoup
import mininorm


def main():
    """ Debug:
	import importlib; import hreader; importlib.reload(hreader)
    """
    page = HReader()
    page.load("calendario.html")
    return page


class HReader:
    """ HTML soup reader """
    exclude_hrefs = ("#",)

    def __init__(self, origin="", name="H"):
        self.name = name
        self._path = ""
        self._origin, self._html = origin, ""
        self.soup = None
        self._norm_opts = "N"	# ASCII-7bit
        self._items = {}

    def origin(self):
        """ Returns the pair: origin (e.g. URL) and HTML """
        return self._origin, self._html

    def texto(self):
        astr = self.soup.get_text(separator="\n", strip=True)
        if self._norm_opts != "N":
            return astr
        return to_ascii7(astr)

    def items(self):
        return self._items

    def load(self, fname, auto=True):
        """ Load HTML from file """
        self._path = fname
        with open(fname, "r", encoding="utf-8") as fdin:
            html = fdin.read()
        self._html = html
        soup = BeautifulSoup(html, "html.parser")
        self.soup = soup
        if not auto:
            return html
        self.parse()
        return html

    def parse(self):
        """ Parse, fill-up _items ...! """
        soup = self.soup
        links = (
            (num, a["href"], a)
            for num, a in enumerate(soup.find_all("a", href=True), 1)
            if a["href"] not in HReader.exclude_hrefs
        )
        dct = {
            "links": links,
            "href-by-num": {},
            "ref-by-path": {},
        }
        for num, href, anchor in links:
            dct["href-by-num"][num] = (href, anchor)
            if href in dct["ref-by-path"]:
                dct["ref-by-path"][href].append(num)
            else:
                dct["ref-by-path"][href] = [num]
        self._items = dct
        return True

    def set_normalize_options(self, opt_str):
        assert isinstance(opt_str, str), "opt_str string!"
        self._norm_opts = opt_str
        return True

def to_ascii7(astr):
    spl = astr.splitlines()
    these = [
        mininorm.to_ascii(line) for line in spl
    ]
    return '\n'.join(these) + '\n'


def extract_calendar(obj):
    """ Tentar...
    <script>
    function downloadCalendar() {
        var calendar = ics();
        $("#calendar-section .calendar-item").each(function (i) {
            var element = $(this);
            var title = element.find('.titleForCalendar').eq(0).text();
            var description = null;
            var location = element.find('.locationForCalendar').eq(0).text();
            var startDate = element.find('.startDateForCalendar').eq(0).text();
            var endDate = element.find('.endDateForCalendar').eq(0).text();
            calendar.addEvent(title, description, location, startDate, endDate);
        })
        calendar.download('calendar');
    }
    </script>
    """
    soup = obj.soup
    events = []
    for item in soup.select("#calendar-section .calendar-item"):
        title = item.select_one(".titleForCalendar")
        location = item.select_one(".locationForCalendar")
        start = item.select_one(".startDateForCalendar")
        end = item.select_one(".endDateForCalendar")
        events.append({
            "title": title.get_text(strip=True) if title else "",
            "location": location.get_text(strip=True) if location else "",
            "start": start.get_text(strip=True) if start else "",
            "end": end.get_text(strip=True) if end else "",
        })
    return events


if __name__ == "__main__":
    main()
