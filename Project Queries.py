#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 17:27:17 2020

@author: rachelfilderman
"""

import csv
import pandas as pd


data = pd.read_csv('cleaned_unemployment.csv',header=0,encoding = "ISO-8859-1")



print(data.head(0))

# columns: unnamed, County, Year, Month, Region, Beneficiaries,  Benefit Amounts (Dollars) , Average Benefits per Beneficiary, Inflation Rate, Adjusted Benefits Per Beneficiary, Adjusted Benefits Amounts, Population, Percent Population on Welfare



print(data.sort_values(by = 'Adjusted Benefits Per Beneficiary', ascending = False).head(10)) 
print(data.sort_values(by = 'Average Benefits per Beneficiary', ascending = False).head(10)) 
# hamilton comes up for both, which is incorrect

# Which county and month/year has the highest spend on benefit
print('Which county and month/year has the highest spend on benefit')
print(data.sort_values(by = 'Adjusted Benefits Amounts', ascending = False).head(10)) 

# Which county and month/year has the highest population
print("Which county and month/year has the highest population")
print(data.sort_values(by = 'Population', ascending = False).head(10)) 
# kings county - brooklyn

# Which county and month/year has the highest percent of people on unemployment
print('Which county and month/year has the highest percent of people on unemployment')
print(data.sort_values(by = 'Percent Population on Welfare', ascending = False).head(10)) 
# queens, niagara, bronx

# Which county since 2001 has had the highest percentage of the county on unemployment per month on average?
print('Which county since 2001 has had the highest percentage of the county on unemployment per month on average?')
print(data.groupby('County').agg({'Percent Population on Welfare': 'mean'}).sort_values(by = 'Percent Population on Welfare', ascending = False))


# Which county since 2001 has had the highest percentage of the county on unemployment per year on average?
print('Which county since 2001 has had the highest percentage of the county on unemployment per year on average?')
print(data.groupby(['County','Year']).agg({'Percent Population on Welfare': 'mean'}).sort_values(by = 'Percent Population on Welfare', ascending = False))


# Which county in any month in 2020 paid out the most benefits? 
print('Which county in any month in 2020 paid out the most benefits?')
print(data[ data['Year']==2020].sort_values(by = 'Adjusted Benefits Amounts', ascending = False).head(10))


# Queens pays the most benefits - taking a look at this county specifically
print('Queens pays the most benefits - taking a look at this county specifically')
print(data[data['County']=='Queens'].sort_values(by = 'Percent Population on Welfare', ascending=False))


# % Population on unemployment per year - looking at top years 
print('% Population on unemployment per year - looking at top years ')
print(data.groupby('Year').agg({'Percent Population on Welfare': 'mean'}).sort_values(by='Percent Population on Welfare',ascending=False))
# highest years are 2020, 2009, 2010, 2011, 2012, 2002, 2003, 2013, 2001, 2008
# is 2020 real? went from 0.83% to 3.89% 
# 2001 -> september 11th, dotcom bubble
# 2007-2009 -> great recession
# 2020 -> COVID 19 recession


# Looking at last 18 months of data - COVID trend
print('Looking at last 18 months of data - COVID trend')
print(data.groupby(['Year', 'Month']).agg({'Percent Population on Welfare': 'mean'}).sort_values(by = ['Year','Month'],ascending = False).head(18))


