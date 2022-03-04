

class query():
    def __init__(self, schoolCode): 
        self.schoolcode = schoolCode

    @property
    def alephcode(self):

        schoolCodeMaps = {
            'AC': 'AMH',
            'MH': 'MHC',
            'HC': 'HAM',
            'SC': 'SMT',
            'UM': 'UMA'
        }
        return schoolCodeMaps[self.schoolcode]

    def __str__(self):
        return f'''
        
SELECT
--ac/um/sc query
'{self.schoolcode}' AS poNumberPrefix,
ord.Z68_Order_NUMBER AS poNumber,
--SUBSTR(ord.Z68_REC_KEY,0,9),
CONCAT('{self.schoolcode}' ,ord.Z68_VENDOR_CODE) AS vendorCode,
ord.Z68_ORDER_Type AS orderType ,
--rr.z13key,
ord.Z68_ORDER_STATUS AS workflowStatus,
-- ord.Z68_ORDER_NUMBER_1, ord.Z68_ORDER_NUMBER_2,
'true' AS reEncumber,
'{self.schoolcode}' AS acqUnitIds,


 ord.Z68_ORDER_GROUP AS orderNote1,
ord.Z68_LIBRARY_NOTE AS orderNote2,
ord.z68_e_note AS orderNote3,
budName.fundName AS orderNote4,
ord.z68_vendor_note AS orderNote5,
ord.z68_subscription_date_from AS subscriptionFrom,
ord.z68_subscription_date_to AS subscriptionTo,
ord.Z68_SUBSCRIPTION_RENEW_DATE AS renewalDate,
--AQUISITION is misspelled in the database.  do not
ord.z68_method_of_AQUISITION AS acquisitionMethod,
ord.z68_invoice_status AS paymentStatus,

ord.z68_vendor_reference_no AS referenceNo,
ord.z68_material_type AS orderFormat,
ord.z68_target_text AS requestor,

ord.Z68_OPEN_DATE,
ord.z68_ORDER_DATE,
ord.Z68_NO_UNITS AS quantityX,
ord.Z68_E_LOCAL_PRICE AS listUnitPrice, 

ord.Z68_ORDER_STATUS_DATE_X,

rr.Z13_TITLE,
rr.author,
ord.z68_isbn
--ord.z68_material_type

-- Umass AND Smith will use the same export critera AS Amherst. To run the Umass query, change the AMH50.Z68 AND AMH50.Z103 to UMA50.Z68 AND UMA.Z103.
-- you will also need to change the org code prefix to UM or SC
FROM {self.alephcode}50.Z68 ord
LEFT JOIN
(
    SELECT brief.Z13_REC_KEY AS z13key , brief.Z13_TITLE,brief.Z13_author AS author ,SUBSTR(lkr.Z103_REC_KEY,6,9) AS ADM_N FROM
    {self.alephcode}50.Z103 lkr
    INNER JOIN
    FCL01.z13 brief
    ON SUBSTR(brief.Z13_REC_KEY, 0,9) = SUBSTR(lkr.Z103_REC_KEY_1,6,9)
    AND lkr.Z103_LKR_TYPE='ADM'
    AND SUBSTR(lkr.Z103_REC_KEY_1,1,5)='FCL01'
) rr
ON SUBSTR(ord.Z68_REC_KEY ,0, 9) = rr.ADM_N
left JOIN
( 
SELECT ordnum, SUBSTR(Z601_REC_KEY ,0, 50) AS fundName FROM 
    (
    SELECT Z601_REC_KEY, SUBSTR(Z601_REC_KEY_3,0,9) AS ordnum, max(SUBSTR(Z601_REC_KEY,50,25)) over (partition by SUBSTR(Z601_REC_KEY_3,0,9)) AS max_open_date FROM {self.alephcode}50.Z601 WHERE SUBSTR(Z601_REC_KEY_3,0,9)<>'000000000'
    ) 
    WHERE max_open_date=SUBSTR(Z601_REC_KEY ,50,25)
) budName
ON rr.ADM_N = budname.ordnum
WHERE
(ord.Z68_ORDER_TYPE = 'S'
AND ord.Z68_ORDER_STATUS = 'SV'
)
OR
(ord.Z68_ORDER_TYPE = 'O'
AND ord.Z68_ORDER_STATUS = 'SV')
OR
(ord.Z68_ORDER_TYPE = 'M'
AND ord.Z68_ORDER_STATUS = 'SV'
AND ord.Z68_OPEN_DATE > 20190701)'''

if __name__ == '__main__':
    x = query('AC')
    print(x)