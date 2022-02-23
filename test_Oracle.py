import unittest
from Oracle import DatabaseQuery

from Query import query

class TestConnection(unittest.TestCase):
    """ suite of tests to make sure sql connection works and returns results"""
    def setUp(self):
        self.conn =  DatabaseQuery(str(query('AC')))
        self.x = self.conn.get_orders()
    def test_connection(self):       
        self.assertTrue(self.conn, 'all config values present')

    def test_query(self):
        #self.conn = dbQuery(login['user'], login["password"], login["dsn"])
        self.assertTrue(len(self.x) >= 1, 'query returns no results ')

    def test_dict_return(self):
        #self.conn = dbQuery(login['user'], login["password"], login["dsn"])
        self.assertEqual(type(self.x[0]), dict, "query does not return dict")

if __name__ == "__main__":
    unittest.main()
