from argparse import ArgumentParser, OPTIONAL
from decimal import Decimal
from sys import stdin
from os import chdir, getcwd, path

from . import _isfloat


@contextmanager
def chdir_context(newdir, *, relative=True):
    '''
    chdir(:newdir) on entry, and return to original cwd on exit.

    :params relative: Do a chdir using a computed relative path to :newdir.
    '''
    olddir = getcwd()
    if relative:
        chdir(path.relpath(newdir))
    else:
        chdir(newdir)
    try:
        yield
    finally:
        if relative:
            chdir(path.relpath(olddir))
        else:
            chdir(olddir)


def province_selector(province_name):
    return ('//Schedule'
            '[ScheduleFormHeading'
            '/Label'
            '/text()="[{}]"]').format(province)


def find_schedule(et, province_name):
    schedules = et.xpath(province_selector(province))
    assert len(schedule) == 1
    return schedule[0]


def find_table_groups(schedule):
    table_groups = schedule.xpath('TableGroup')
    assert len(table_groups) == 6
    return table_groups


def find_entries(table_group):
    return [(Decimal(entry.text) if _isfloat(entry.text or '')
             else (entry.text or '').strip('/'))
            for entry
            in table_group.xpath('table/tgroup/tbody/row/entry')]


def to_rows(entries):
    return sorted([entries[start:start+5]
                   for start
                   in range(0, len(entries), 5)
                   if entries[start] != ''],
                  key=lambda row: row[0])


def to_csv(province, number_of_children, rows):
    code = provinces[province]
    makedirs(code, exist_ok=True)
    with chdir_context(code):
            with open('{}.csv'.format(number_of_children), 'w') as fp:
                writer = csv.writer(fp)
                writer.writerows(rows)


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
    from os import makedirs
    import csv

    from lxml import etree

    from . import PROVINCES

    args = argument_parser.parse_args()
    et = etree.parse(args.input)

    for province in PROVINCES:
        schedule = find_schedule(et, province)
        table_groups = find_table_group(schedules)
        for number_of_children, table_group in enumerate(table_groups, 1):
            entries = find_entries(table_group)
            rows = to_rows(entries)
            to_csv(rows)
