'''make a dict ready for import from a tsv'''
from csv import DictReader
import json

with open('Data/material_types.tsv','r', encoding='utf8') as tsv:
    output = {}
    target_tsv = DictReader(tsv, delimiter='\t')
    for row in target_tsv:
        mergeName = row['Material_Type'].rstrip() + row['School_code'].rstrip()
        x = [row['FOLIO'], row['order_type']]
        output.update({mergeName: x})
    
    target  = open('Data/material.py','w') 
    json.dump(output,target, indent=4)




