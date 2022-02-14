'''run all the things'''
from csv import DictWriter
from Oracle import dbQuery
from Query import query
from rowClean import cleanRow


if __name__ == "__main__":
    print('working...')
    conn = dbQuery(str(query("AC")))
    conn.orders
    headers = ([x[0] for x in conn.headers])
    del headers[7:12]
    headers.append('notes')
    print(headers)
    with open('dictOutput.csv','w', newline='', encoding='utf8') as target:
        dictwrite = DictWriter(target, fieldnames=headers)
        dictwrite.writeheader()
        for line in conn.orders:
            dictwrite.writerow(cleanRow(line))
