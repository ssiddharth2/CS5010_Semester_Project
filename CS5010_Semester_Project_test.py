

import unittest

import os
os.getcwd()
os.chdir('c:\\Users\\emkmu\\OneDrive\\Documents\\SDS\\CS 5010\\Project\\CS5010_Semester_Project')

from CS5010_Semester_Project import *


class Unemployment(unittest.TestCase):
    # Test to make sure all null FIPS codes were removed.
    def test_FIPS_isnot_null(self):
        
        self.assertIsNotNone(county_clean['FIPS Code'])
        
    # Test to ensure all FIPS codes for one county are the same and equal the correct value
    def test_FIPS_is_correct(self):
        
        self.assertEqual(county_clean['FIPS Code'][county_clean['County']=='Queens'].mean(),36081)
    
    # Test to check the data starts with the year 2001
    def test_min_year_is_2001(self):
        
        self.assertEqual(county_clean['Year'].min(),2001)       
        
if __name__ == '__main__':
    unittest.main()   