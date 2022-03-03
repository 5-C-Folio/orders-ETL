

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
'HC' AS poNumberPrefix,
ord.Z68_Order_NUMBER AS poNumber,
--SUBSTR(ord.Z68_REC_KEY,0,9),
CONCAT('HC' ,ord.Z68_VENDOR_CODE) AS vendorCode,
ord.Z68_ORDER_Type AS orderType ,
--rr.z13key,
ord.Z68_ORDER_STATUS AS workflowStatus,
-- ord.Z68_ORDER_NUMBER_1, ord.Z68_ORDER_NUMBER_2,
'true' AS reEncumber,
'HC' AS acqUnitIds,


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
FROM HAM50.Z68 ord
LEFT JOIN
(
    SELECT brief.Z13_REC_KEY AS z13key , brief.Z13_TITLE,brief.Z13_author AS author ,SUBSTR(lkr.Z103_REC_KEY,6,9) AS ADM_N FROM
    HAM50.Z103 lkr
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
    SELECT Z601_REC_KEY, SUBSTR(Z601_REC_KEY_3,0,9) AS ordnum, max(SUBSTR(Z601_REC_KEY,50,25)) over (partition by SUBSTR(Z601_REC_KEY_3,0,9)) AS max_open_date FROM HAM50.Z601 WHERE SUBSTR(Z601_REC_KEY_3,0,9)<>'000000000'
    ) 
    WHERE max_open_date=SUBSTR(Z601_REC_KEY ,50,25)
) budName
ON rr.ADM_N = budname.ordnum
WHERE

ord.Z68_ORDER_STATUS != 'CLS'
and(
ord.Z68_REC_KEY not in (
-- restriction 1
SELECT ord1.Z68_REC_KEY FROM
    HAM50.Z68 ord1
    inner join (
    select Z00R_DOC_NUMBER, Z00R_TEXT, substr(Z103_REC_KEY,6,9) as ADM_N from HAM50.Z103, FCL01.Z00R
where Z00R_DOC_NUMBER=substr(Z103_REC_KEY_1,6,9)
and Z103_LKR_TYPE='ADM'
and substr(Z103_REC_KEY_1,1,5)='FCL01'
and substr(Z00R_FIELD_CODE,0,3) ='FMT'
) rr
    on substr(ord1.Z68_REC_KEY ,0, 9) = rr.ADM_N
 left join(
 select Z00R_DOC_NUMBER, Z00R_TEXT, substr(Z103_REC_KEY,6,9) as ADM_N from HAM50.Z103, FCL01.Z00R
where Z00R_DOC_NUMBER=substr(Z103_REC_KEY_1,6,9)
and Z103_LKR_TYPE='ADM'
and substr(Z103_REC_KEY_1,1,5)='FCL01'
and substr(Z00R_FIELD_CODE,0,3) ='STA') sta
on substr(ord1.Z68_REC_KEY ,0, 9) = sta.ADM_N
    WHERE
    rr.z00r_text like 'BK%'
    and substr(ord1.z68_material_type,0,1 )= 'M'
    and ord1.z68_order_type= 'M'
    and  ord1.Z68_OPEN_DATE < 20170630
    and sta.z00r_text is NULL
    and ord1.Z68_ORDER_STATUS IN ('CLS','LC', 'VC')
    )
  --restriction2
 OR  ord.Z68_REC_KEY not in ( 
 SELECT ord1.Z68_REC_KEY FROM
    HAM50.Z68 ord1
    inner join (
    select Z00R_DOC_NUMBER, Z00R_TEXT, substr(Z103_REC_KEY,6,9) as ADM_N from HAM50.Z103, FCL01.Z00R
where Z00R_DOC_NUMBER=substr(Z103_REC_KEY_1,6,9)
and Z103_LKR_TYPE='ADM'
and substr(Z103_REC_KEY_1,1,5)='FCL01'
and substr(Z00R_FIELD_CODE,0,3) ='FMT'
) rr
    on substr(ord1.Z68_REC_KEY ,0, 9) = rr.ADM_N
 left join(
 select Z00R_DOC_NUMBER, Z00R_TEXT, substr(Z103_REC_KEY,6,9) as ADM_N from HAM50.Z103, FCL01.Z00R
where Z00R_DOC_NUMBER=substr(Z103_REC_KEY_1,6,9)
and Z103_LKR_TYPE='ADM'
and substr(Z103_REC_KEY_1,1,5)='FCL01'
and substr(Z00R_FIELD_CODE,0,3) ='STA') sta
on substr(ord1.Z68_REC_KEY ,0, 9) = sta.ADM_N
    WHERE
    rr.z00r_text like 'MU%'
    and substr(ord1.z68_material_type,0,1 )= 'A'
    and ord1.z68_order_type= 'M'
    and  ord1.Z68_OPEN_DATE < 20170630
    and sta.z00r_text is NULL
    and ord1.Z68_ORDER_STATUS IN ('CLS','LC', 'VC')
    )
OR    
--restriction 3
ord.Z68_REC_KEY not in ( 
 SELECT ord1.Z68_REC_KEY FROM
    HAM50.Z68 ord1
    inner join (
    select Z00R_DOC_NUMBER, Z00R_TEXT, substr(Z103_REC_KEY,6,9) as ADM_N from HAM50.Z103, FCL01.Z00R
where Z00R_DOC_NUMBER=substr(Z103_REC_KEY_1,6,9)
and Z103_LKR_TYPE='ADM'
and substr(Z103_REC_KEY_1,1,5)='FCL01'
and substr(Z00R_FIELD_CODE,0,3) ='FMT'
) rr
    on substr(ord1.Z68_REC_KEY ,0, 9) = rr.ADM_N
 left join(
 select Z00R_DOC_NUMBER, Z00R_TEXT, substr(Z103_REC_KEY,6,9) as ADM_N from HAM50.Z103, FCL01.Z00R
where Z00R_DOC_NUMBER=substr(Z103_REC_KEY_1,6,9)
and Z103_LKR_TYPE='ADM'
and substr(Z103_REC_KEY_1,1,5)='FCL01'
and substr(Z00R_FIELD_CODE,0,3) ='STA') sta
on substr(ord1.Z68_REC_KEY ,0, 9) = sta.ADM_N
    WHERE
    rr.z00r_text like 'VM%'
    and substr(ord1.z68_material_type,0,1 )= 'V'
    and ord1.z68_order_type= 'M'
    and  ord1.Z68_OPEN_DATE < 20170630
    and sta.z00r_text is NULL
    and ord1.Z68_ORDER_STATUS IN ('CLS','LC', 'VC')
    ))
    '''

if __name__ == '__main__':
    x = query('AC')
    print(x)