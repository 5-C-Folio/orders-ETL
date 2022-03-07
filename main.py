"""run all the things"""
from csv import DictWriter
from Oracle import DatabaseQuery
from Query import query
from rowClean import process
from sys import argv
from datetime import datetime

if __name__ == "__main__":
    
    school_code = argv[1]
    if school_code not in ['AC', 'MH', 'HC', 'SC', 'UM']:
        print('invalid code')
    if school_code == 'MH':
        from QueryMH import query
    elif school_code == 'HC':
        from Queryham import query
    else:
        from Query import query


    print(query(school_code))
    now = datetime.now()

    conn = DatabaseQuery(str(query(school_code)))
    result = conn.get_orders()
    column_headers = conn.headers
    del column_headers[7:12]
    column_headers.remove("ORDERFORMAT")
    column_headers.remove("Z68_ORDER_STATUS_DATE_X")
    column_headers = column_headers + [
        'notes', 'checkinItems', 'manualPo', 'isSubscription', 'orderFormat',
        'materialType', 'closeReason', "closeReasonNote", 'paymentStatus', 'receiptStatus', 'productIdType'
    ]
    print(column_headers)
    with open(f'{school_code}-acq-{now.strftime("%b-%d-%H")}.csv', 'w', newline='', encoding='utf8') as target:
        dictwrite = DictWriter(target,
                               fieldnames=column_headers,
                               delimiter=',')
        dictwrite.writeheader()
        for line in result:
            dictwrite.writerow(process(line))
    
