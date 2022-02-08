import unittest
from Oracle import dbQuery
from config import login
from Query import query

class testconnection(unittest.TestCase):
    def setUp(self):
        self.conn =  dbQuery(str(query('AC')))
        self.x = self.conn.orders
    def test_connection(self):
       
        self.assertTrue(self.conn, 'all config values present')

    def test_query(self):
        #self.conn = dbQuery(login['user'], login["password"], login["dsn"])
        self.assertTrue(len(self.x) >= 1, 'query returns no results ')

    def test_dictReturn(self):
        #self.conn = dbQuery(login['user'], login["password"], login["dsn"])
        self.assertEqual(type(self.x[0]), dict, "query does not return dict")

    
if __name__ == "__main__":
    unittest.main()