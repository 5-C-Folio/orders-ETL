from material import order_materials
from functools import lru_cache
from Acq_method import acq_methods


def deleteKeys(li, d):
    for k in li:
        d.pop(k)


@lru_cache(4)
def material_map(Z68_MATERIAL_TYPE, ACQUNITIDS):
    try:
        material_key = Z68_MATERIAL_TYPE.rstrip() + ACQUNITIDS
        folio_material = order_materials[material_key][0]
        folio_format = order_materials[material_key][1]
    except AttributeError:
        folio_material = 'ERROR'
        folio_format = 'ERROR'
    return [{"orderFormat": folio_format}, {'materialType': folio_material}]

    print(folio_material, folio_format)


@lru_cache(4)
def method_map(method, ACQUNITIDS):
    try:
        method_key = method.rstrip() + ACQUNITIDS
        return acq_methods[method_key]
    except AttributeError:
        return 'ERROR'


def pay_receipt(row):
    if row['WORKFLOWSTATUS'] in ['LC ', 'VC ']:
        row.update({'paymentStatus': 'fully paid', 'receiptStatus' : 'fully received'})
    elif row['ORDERTYPE'] == 'M' and row['WORKFLOWSTATUS'].rstrip() == 'SV':
        row.update({'paymentStatus': 'pending', 'receiptStatus' : 'pending'})
    else:
        row.update({'paymentStatus': '', 'receiptStatus' : ''})
    return row






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
    deleteKeys(
        ['ORDERNOTE1', 'ORDERNOTE2', 'ORDERNOTE3', 'ORDERNOTE4', 'ORDERNOTE5'],
        row)
    row['notes'] = '; '.join(notes)
    return row


def update_values(row):
    if row['ORDERTYPE'] in ['S', 'O']:
        row.update({'checkinItems': 'Independent order and receipt quantity'})
    else:
        row.update({'checkinItems': 'Synchronized order and receipt quantity'})
    if row['ORDERTYPE'] in ['O', 'M']:
        row.update({"isSubscription": False})
    elif row['ORDERTYPE'] == 'S':
        row.update({"isSubscription": True})
    if row["PONUMBERPREFIX"] == 'MH' and row["ORDERTYPE"] in ["S", "O"] and row["WORKFLOWSTATUS"] == 'SV ':
        row.update({'RENEWALDATE': '20991231'})
    row.update({'manualPo': True})
    if int(row['RENEWALDATE']) < 20220223 and int(
            row['RENEWALDATE']) != 0 and row["WORKFLOWSTATUS"] == 'SV ':
        row.update({'RENEWALDATE': 20991231})
    orderFormat, orderMaterial = material_map(row['ORDERFORMAT'],
                                             row['ACQUNITIDS'])
    try:                                         
        row.update({
        'LISTUNITPRICE':
        f'{int(row["LISTUNITPRICE"][:-2])}.{row["LISTUNITPRICE"][-2:]}'
    })
    except:
        pass
    row.update(orderFormat)
    row.update(orderMaterial)
    row.update({
        'ACQUISITIONMETHOD':
        method_map(row['ACQUISITIONMETHOD'].rstrip(), row['ACQUNITIDS'])
    })

    if row['ORDERTYPE'].rstrip() == 'M':
        row.update({'ORDERTYPE': 'one-time'})
    elif row['ORDERTYPE'].rstrip() in ['S', 'O']:
        row.update({'ORDERTYPE': 'ongoing'})
    row.pop('ORDERFORMAT')
    return row


def reason_close(row):

    if row['WORKFLOWSTATUS'] == 'LC ':
        row.update({"WORKFLOWSTATUS": "Closed"})
        row.update({"closeReason": "Cancelled"})
        row.update({
            "closeReasonNote":
            f"Library Cancelled {row['Z68_ORDER_STATUS_DATE_X']}"
        })
        row.update({'RENEWALDATE': 0})
        row.update({'REENCUMBER': False})
    elif row['WORKFLOWSTATUS'] == 'VC ':
        row.update({"WORKFLOWSTATUS": "Closed"})
        row.update({
            "closeReason":
            f"Vendor Cancelled"
        })
        row.update({
            "closeReasonNote":
            f"Vendor Cancelled {row['Z68_ORDER_STATUS_DATE_X']}"
        })
        row.update({'RENEWALDATE': 0})
        row.update({'REENCUMBER': False})
    else:
        row.update({'WORKFLOWSTATUS': 'Pending'})
        row.update({"closeReason": ''})
        row.update({"closeReasonNote": ''})

    row.pop('Z68_ORDER_STATUS_DATE_X')
    return row


def process(row):
    row = pay_receipt(row)
    row = row_clean(row)
    row = update_values(row)
    row = reason_close(row)
    return row
