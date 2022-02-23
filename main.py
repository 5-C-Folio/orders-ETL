"""run all the things"""
from csv import DictWriter
from Oracle import DatabaseQuery
from Query import query
from rowClean import process









if __name__ == "__main__":
    print('working...')
    conn = DatabaseQuery(str(query("SC")))
    result = conn.get_orders()
    column_headers = conn.headers
    del column_headers[7:12]
    column_headers  =  column_headers +['notes','checkinItems', 'manualPo', 'isSubscription']
    print(column_headers)
    with open('dictOutput.csv', 'w', newline='', encoding='utf8') as target:
        dictwrite = DictWriter(target, fieldnames=column_headers)
        dictwrite.writeheader()
        for line in result:
            dictwrite.writerow(process(line))
