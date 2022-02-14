



['PONUMBERPREFIX', 'PONUMBER', 'VENDORCODE',
    'ORDERTYPE', 'WORKFLOWSTATUS', 'REENCUMBER',
    'ACQUNITIDS', 'ORDERNOTE1', 'ORDERNOTE2', 
    'ORDERNOTE3', 'ORDERNOTE4', 'ORDERNOTE5', 
    'SUBSCRIPTIONFROM', 'SUBSCRIPTIONTO', 'RENEWALDATE',
    'ACQUISITIONMETHOD', 'PAYMENTSTATUS', 'REFERENCENO',
    'ORDERFORMAT', 'REQUESTOR',
    'Z68_OPEN_DATE', 'Z68_ORDER_DATE', 'QUANTITYX',
    'LISTUNITPRICE', 'Z68_ORDER_STATUS_DATE_X', 
    'Z13_TITLE', 'AUTHOR', 'Z68_ISBN', 'Z68_MATERIAL_TYPE']

def deleteKeys(li, d):
    for k in li:
        d.pop(k)
        
  


def cleanRow(row):
    row['PONUMBER'] = row['PONUMBER'].rstrip()
    notes = []
    if   row['ORDERNOTE1']:
         notes.append(f'order group: {row["ORDERNOTE1"].rstrip()};')
    if   row['ORDERNOTE2']:
         notes.append(f'library note: {row["ORDERNOTE2"].rstrip()};')
    if   row['ORDERNOTE3']:
         notes.append(f'e_note: {row["ORDERNOTE3"].rstrip()};')
    if   row['ORDERNOTE4']:
         notes.append(f'fund name: {row["ORDERNOTE4"].rstrip()};')
    if   row['ORDERNOTE5']:
         notes.append(f'vendor note: {row["ORDERNOTE5"].rstrip()};')
    deleteKeys(['ORDERNOTE1', 'ORDERNOTE2', 
    'ORDERNOTE3', 'ORDERNOTE4', 'ORDERNOTE5'], row)
    row['notes']=' '.join(notes)
    return row

    