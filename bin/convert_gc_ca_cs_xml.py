#! /usr/bin/env python3

import csv
from os import chdir, makedirs
from sys import stdin
from decimal import Decimal
from argparse import ArgumentParser, OPTIONAL

from lxml import etree


def isfloat(s):
    try:
        float(s)
    except:
        return False
    else:
        return True


argument_parser = ArgumentParser(
    'Justice Canada child support tables extractor')
# E.g. http://laws-lois.justice.gc.ca/eng/XML/SOR-97-175.xml
argument_parser.add_argument('input',
                             help='Name of XML-formatted family law document',
                             default=stdin.buffer,
                             nargs=OPTIONAL)
args = argument_parser.parse_args()

et = etree.parse(args.input)

provinces = {'ONTARIO': 'ontario',
             'QUEBEC/QUÉBEC': 'quebec',
             'NOVA SCOTIA/NOUVELLE-ÉCOSSE': 'nova_scotia',
             'NEW BRUNSWICK/NOUVEAU-BRUNSWICK': 'new_brunswick',
             'MANITOBA': 'manitoba',
             'BRITISH COLUMBIA/COLOMBIE-BRITANNIQUE': 'british_columbia',
             'PRINCE EDWARD ISLAND/ÎLE-DU-PRINCE-ÉDOUARD': 'prince_edward_island',
             'SASKATCHEWAN': 'saskatchewan',
             'ALBERTA': 'alberta',
             'NEWFOUNDLAND AND LABRADOR/TERRE-NEUVE-ET-LABRADOR': 'newfoundland_and_labrador',
             'YUKON': 'yukon',
             'NORTHWEST TERRITORIES/TERRITOIRES DU NORD-OUEST': 'northwest_territories',
             'NUNAVUT': 'nunavut'}

for province, code in provinces.items():
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
        entries = [(Decimal(entry.text) if isfloat(entry.text or '') else (entry.text or '').strip('/'))
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
