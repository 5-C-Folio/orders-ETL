import unittest
import Query


class TestQuery(unittest.TestCase):
    
    def test_schoolCode(self):
        self.assertEqual(type(str(Query.query('AC'))), str, 'query is not a string' )

    def test_alephMap(self):
        self.assertEqual(Query.query('AC').alephcode, 'AMH', "mapping is incorrect")

    def test_schoolcode(self):
        self.assertEqual(Query.query('AC').schoolcode, 'AC', "Input does not equal properyt")

    def test_query_format(self):
        self.assertTrue('AMH50.Z68' in str(Query.query('AC')), 'AMH not in query string')


if __name__ == "__main__":
    unittest.main()

    