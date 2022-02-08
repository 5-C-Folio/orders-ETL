from Oracle import dbQuery
from Query import query
from csv import DictWriter


if __name__ == "__main__":
    
    conn = dbQuery(str(query("AC")))
    conn.orders
    headers = ([x[0] for x in conn.headers])
    with open('dictOutput','w', newline='', encoding='utf8') as target:
        dictwrite = DictWriter(target, fieldnames=headers)
        dictwrite.writeheader()
        for line in conn.orders:
            dictwrite.writerow(line)
