import os
os.getcwd()

import unittest

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
    
    # Test to make sure columns were deleted and column count is correct
    def test_column_count(self):
        
        self.assertEqual(len(county_clean.columns), 13) 
        
    # Test to make sure no percentage is over 100%    
    def test_percent_max(self):
        
        self.assertTrue(max(county_clean['Percent Population on Welfare'])<=100)
   
    # Test to make sure our inflation calculator is accurate
    def test_inflation_calculation(self):
        avgben = county_clean['Average Benefits per Beneficiary'][(county_clean['County']=='Queens')&(county_clean['Year']==2002)&(county_clean['Month']==6)].sum()
        inflation= county_clean['Inflation Rate'][(county_clean['County']=='Queens')&(county_clean['Year']==2002)&(county_clean['Month']==6)].sum()

        adjben = round(((avgben/inflation)*257.797),2)
        
        
        self.assertEqual(adjben, 1364.70)
        
    # Test to make sure our % population on benefits is accurate  
    def test_beneficiaries_per_population_calculation(self):
        population = county_clean['Population'][(county_clean['County']=='Queens')&(county_clean['Year']==2002)&(county_clean['Month']==6)].sum()
        beneficiaries = county_clean['Beneficiaries'][(county_clean['County']=='Queens')&(county_clean['Year']==2002)&(county_clean['Month']==6)].sum()
        
        ben_per_pop = round((beneficiaries/population)*100,2)
        
        self.assertEquals(ben_per_pop, 1.15)
        

        
if __name__ == '__main__':
    unittest.main()   
    
