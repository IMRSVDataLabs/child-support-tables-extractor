from argparse import ArgumentParser, OPTIONAL
from sys import stdin


argument_parser = ArgumentParser(
    'Justice Canada child support tables extractor')
# E.g. http://laws-lois.justice.gc.ca/eng/XML/SOR-97-175.xml
argument_parser.add_argument('input',
                             help='Name of XML-formatted family law document',
                             default=stdin.buffer,
                             nargs=OPTIONAL)


# We still want to be able to test the above programmatically without running
# the script.
if __name__ == '__main__':  # pragma: no cover
    from os import chdir, makedirs
    from decimal import Decimal
    import csv

    from lxml import etree

    from . import PROVINCES, _isfloat

    args = argument_parser.parse_args()
    et = etree.parse(args.input)


    for province, code in PROVINCES.items():
        schedule = et.xpath('//Schedule'
                            '[ScheduleFormHeading'
                            '/Label'
                            '/text()="[{}]"]'.format(province))
        assert len(schedule) == 1
        schedule = schedule[0]
        table_groups = schedule.xpath('TableGroup')
        assert len(table_groups) == 6

        makedirs(code, exist_ok=True)
        chdir(code)
        for number_of_children, table_group in enumerate(table_groups, 1):
            entries = [(Decimal(entry.text) if _isfloat(entry.text or '') else (entry.text or '').strip('/'))
                       for entry
                       in table_group.xpath('table/tgroup/tbody/row/entry')]
            rows = sorted([entries[start:start+5]
                           for start
                           in range(0, len(entries), 5)
                           if entries[start] != ''],
                          key=lambda row: row[0])

            with open('{}.csv'.format(number_of_children), 'w') as fp:
                writer = csv.writer(fp)
                writer.writerows(rows)
        chdir('..')
