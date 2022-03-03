'''make a dict ready for import from a tsv'''
from csv import DictReader
import json

with open('Data/acq_method.tsv', 'r', encoding='utf8') as tsv:
    output = {}
    target_tsv = DictReader(tsv, delimiter='\t')
    for row in target_tsv:
        mergeName = row['code'].rstrip() + row['school'].rstrip()
        x = row['folio']
        output.update({mergeName: x})

    target = open('Data/acq_method.py', 'w')
    json.dump(output, target, indent=4)
