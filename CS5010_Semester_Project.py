#!/usr/bin/env python
# coding: utf-8

import pandas as pd

#Pull in county population data from web
counties = pd.read_html('https://www.newyork-demographics.com/counties_by_population')
county_data=counties[0]
county_data["County"]=[county.replace(" County","").strip() for county in county_data["County"]]
county_data = county_data[county_data.County.str.contains('United States Census') == False]

#Pull in predownloaded .csv file on umployment
data=pd.read_csv("unemp.csv")

#Merge county and unemployment data on county name
county_clean=pd.merge(county_data, data, how='inner', on='County', left_on=None, right_on=None,
         left_index=False, right_index=False, sort=True,
         suffixes=('_x', '_y'), copy=True, indicator=False,
         validate=None)

#Remove commas in numbers
county_clean.iloc[:,6]= [int(amount.replace(",","").strip()) for amount in
                                            county_clean.iloc[:,6]]
county_clean.iloc[:,7]= [int(amount.replace(",","").strip()) for amount in
                                            county_clean.iloc[:,7]]
#Create new column with benefits per beneficiary
county_clean["Average Benefits per Beneficiary"]=county_clean.iloc[:,7]/county_clean.iloc[:,6] #need to convert to int

#Pull in inflation data from web
inf_data=pd.read_html('https://www.usinflationcalculator.com/inflation/consumer-price-index-and-annual-percent-changes-from-1913-to-2008/')[0]
inf_data.columns=inf_data.iloc[1]
inf_data=inf_data.iloc[2:,0:13]
inf_data=inf_data.melt(id_vars=['Year'], value_vars=inf_data.columns[1:])
inf_data["Year"]=[int(year)for year in inf_data["Year"]]
inf_data=inf_data[inf_data["Year"]>=2000]
inf_data=inf_data.sort_values("Year")
inf_data = inf_data.replace(["Jan","Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"],[1,2,3,4,5,6,7,8,9,10,11,12])
inf_data = inf_data.rename(columns={1: "Month"})

#Merge inflation data into unemployment data 
county_clean=pd.merge(county_clean, inf_data, how='left', on=['Year','Month'], left_on=None, right_on=None,
         left_index=False, right_index=False, sort=True,
         suffixes=('_x', '_y'), copy=True, indicator=False,
         validate=None)

#Rename inflation rate and round to nearest hundredth
county_clean = county_clean.rename(columns={'value': 'Inflation Rate'})
county_clean["Inflation Rate"]=[float(data) for data in county_clean["Inflation Rate"]]

#Create new columns that adjust by inflation in 2020 dollars
county_clean["Adjusted Benefits Per Beneficiary"] = (county_clean["Average Benefits per Beneficiary"]/county_clean["Inflation Rate"])*257.797
county_clean["Adjusted Benefits Amounts"] = (county_clean.iloc[:,7]/county_clean["Inflation Rate"])*257.797

#Pull in other population info from web
population_data=pd.read_csv("Annual_Population_Estimates_for_New_York_State_and_Counties__Beginning_1970.csv")
population_data=population_data[population_data["Year"]>=2001]
population_data["Geography"]=[county.replace(" County","").strip() for county in population_data["Geography"]]
population_data = population_data.rename(columns={"Geography": "County"})

#Merge new population data into unemployment
county_clean=pd.merge(county_clean, population_data, how='left', on=['Year','County'], left_on=None, right_on=None,
         left_index=False, right_index=False, sort=True,
         suffixes=('_x', '_y'), copy=True, indicator=False,
         validate=None)

#Merge populations to create a full population list of valid numbers
county_clean.loc[county_clean["Year"] == 2020,"Population_y"]=county_clean.loc[county_clean["Year"] == 2020,"Population_x"]
county_clean['FIPS Code'] = county_clean['FIPS Code'].fillna(county_clean.groupby('County')['FIPS Code'].transform('mean'))

checker=county_clean['Population_y'].isna()
checker=checker[checker==True]

#Remove unnecessary columns
county_clean=county_clean.drop(['Rank','Population_x','Program Type'],axis=1)

#Rename relevant population
county_clean = county_clean.rename(columns={'Population_y': 'Population'})

#Turn population into an int and then create column to adjust for beneficiaries per capita
county_clean["Population"]=[int(population)for population in county_clean["Population"]]
county_clean["Percent Population on Welfare"]=(county_clean["Beneficiaries"]/county_clean["Population"])*100

#Round all data to the nearest hundredth
county_clean=county_clean.round(2)

#Create a new .csv
county_clean.to_csv("cleaned_unemployment.csv")

