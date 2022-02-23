
from functools import lru_cache

def deleteKeys(li, d):
    for k in li:
        d.pop(k)





def row_clean(row):
    '''Merge note fields together and delete the old fields'''
    row['PONUMBER'] = row['PONUMBER'].rstrip()
    notes = []
    if row['ORDERNOTE1']:
        notes.append(f'order group: {row["ORDERNOTE1"].rstrip()}')
    if row['ORDERNOTE2']:
        notes.append(f'library note: {row["ORDERNOTE2"].rstrip()}')
    if row['ORDERNOTE3']:
        notes.append(f'e_note: {row["ORDERNOTE3"].rstrip()}')
    if row['ORDERNOTE4']:
        notes.append(f'fund name: {row["ORDERNOTE4"].rstrip()}')
    if row['ORDERNOTE5']:
        notes.append(f'vendor note: {row["ORDERNOTE5"].rstrip()}')
    deleteKeys(['ORDERNOTE1', 'ORDERNOTE2',
                'ORDERNOTE3', 'ORDERNOTE4', 'ORDERNOTE5'], row)
    row['notes'] = '; '.join(notes)            
    return row
    
    


def update_values(row):
    if row['ORDERTYPE'] in ['S', 'O'] :
        row.update({'checkinItems': 'Independent order and receipt quantity'})
    else:
        row.update({'checkinItems':'Synchronized order and receipt quantity'})
    
    row.update({'WORKFLOWSTATUS': 'Pending'})
    row.update({'manualPo': True})
    return row

def process(row):
    row = row_clean(row)
    row = update_values(row)
    return row
