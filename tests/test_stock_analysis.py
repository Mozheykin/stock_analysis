import unittest
import os
import sys
sys.path.append(os.getcwd())
from stock_analysis import TA


class TA_Test(unittest.TestCase):
    def setUp(self):
        self.ta = TA(symbols=['GAZP', 'POLY'])

    def test_stock_analysis(self):
        self.assertEqual(list(self.ta.alert()), [])
        self.ta.last['GAZP']['rec'] = 'STRONG_BUY'
        self.ta.RECOMMENDATIONS.append('BUY')
        self.ta.RECOMMENDATIONS.append('SELL')
        self.assertEqual(list(self.ta.alert())[0].keys(), ({'GAZP': {'rec': 'BUY'}}).keys())

    def test_errors(self):
        self.ta = TA(symbols='any')
        with self.assertRaises(ValueError):
            list(self.ta.alert())


if __name__ == '__main__':
    unittest.main()
