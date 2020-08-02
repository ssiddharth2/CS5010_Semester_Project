#!/usr/bin/env python
# coding: utf-8


# libraries
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_style("white")
import pandas as pd
import plotly.express as px
import datetime as dt
my_dpi=96

#Read in our .csv file
data = pd.read_csv("cleaned_unemployment.csv")

#Reformat .csv info to create a date that is workable
dt.datetime.strptime("2020 1", '%Y %m')
data['time']=[dt.datetime.strptime(str(year)+' ' + str(month), '%Y %m') for year,month in zip(data['Year'],data['Month'])]

#Organizing data by Region and Date
modified_data= data.sort_values(['time'])
modified_data=modified_data.groupby(['Region',"time"])['Adjusted Benefits Amounts','Population','Beneficiaries'].sum()
modified_data=modified_data.round(2)
modified_data=modified_data.reset_index()

#Creating new per capita columns based off of new summed groups
modified_data['Adjusted Benefits Per Beneficiary']=modified_data['Adjusted Benefits Amounts']/modified_data['Beneficiaries']
modified_data['Percent Population on Welfare']=(modified_data['Beneficiaries']/modified_data['Population'])*100
modified_data=modified_data.sort_values('time')
modified_data=modified_data.round(2)

#Creating an NYC only dataset used further below
nyc_data=data[data["Region"]=="New York City"]

#Renaming orginal data and creating column to delineate in and out of NYC
new_data=data
new_data["is New York"]= ["New York City" if data=="New York City" else "Rest of New York" for data in new_data['Region']]

#Grouping data by inside and outside of NYC and creating new percent population on welfare
new_data=new_data.groupby(['is New York','time','Month','Year'])['Adjusted Benefits Amounts','Population','Beneficiaries'].sum()
new_data=new_data.reset_index()
new_data=new_data.sort_values('time')
new_data['Percent Population on Welfare']=(new_data["Beneficiaries"]/new_data["Population"])*100



def get_dataset():
    #Creates dataset with datetime formatted column and organized adjusted benefits
    the_data = pd.read_csv("cleaned_unemployment.csv")
    the_data['time']=[dt.datetime.strptime(str(year)+' ' + str(month), '%Y %m') for year,month in 
                      zip(the_data['Year'],the_data['Month'])]
    the_data= the_data.sort_values(['time'])
    the_data=the_data.groupby(['County',"time","Month","Year"])['Adjusted Benefits Amounts','Population','Beneficiaries'].sum()
    the_data=the_data.round(2)
    the_data=the_data.reset_index()
    the_data['Adjusted Benefits Per Beneficiary']=the_data['Adjusted Benefits Amounts']/the_data['Beneficiaries']
    the_data['Percent Population on Welfare']=(the_data['Beneficiaries']/the_data['Population'])*100
    the_data=the_data.sort_values('time')
    the_data=the_data.round(2)
    return the_data


def get_region_dataset():
    #Creates dataset with datetime formatted column and organized by region and adjusted benefits
    the_data = pd.read_csv("cleaned_unemployment.csv")
    the_data['time']=[dt.datetime.strptime(str(year)+' ' + str(month), '%Y %m') for year,month in 
                      zip(the_data['Year'],the_data['Month'])]
    the_data= the_data.sort_values(['time'])
    the_data=the_data.groupby(['Region',"time","Month","Year"])['Adjusted Benefits Amounts','Population','Beneficiaries'].sum()
    the_data=the_data.round(2)
    the_data=the_data.reset_index()
    the_data['Adjusted Benefits Per Beneficiary']=the_data['Adjusted Benefits Amounts']/the_data['Beneficiaries']
    the_data['Percent Population on Welfare']=(the_data['Beneficiaries']/the_data['Population'])*100
    the_data=the_data.sort_values('time')
    the_data=the_data.round(2)
    return the_data



def create_scatterplot_counties(start_point,end_point,county_lst,option_number):
    #Creates 4 types of scatterplot and can be narrowed by time and a subset of counties
    counties=county_lst
    print(counties)
    data=get_dataset()
    start=start_point.split()
    end=end_point.split()
    data["Month"]=data["Month"].replace([1,2,3,4,5,6,7,8,9,10,11,12],["Jan","Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"])
    data["Month"]=[month+" "+str(year) for month,year in zip(data["Month"],data["Year"])]
    start=dt.datetime.strptime(start[1]+' ' + start[0], '%Y %B')
    end=dt.datetime.strptime(end[1]+' ' + end[0], '%Y %B')
    data=data[data['time']>=start]
    data=data[data['time']<=end]
    data=data.loc[data['County'].isin(counties),:]
    if(option_number==1):
        fig= px.line(data, x="Month", y="Percent Population on Welfare", color='County')
        fig.show()
    elif(option_number==2):
        fig= px.line(data, x="Month", y="Adjusted Benefits Per Beneficiary", color='County')
        fig.show()
    elif(option_number==3):
        fig= px.line(data, x="Month", y="Adjusted Benefits Amounts", color='County')
        fig.show()
    elif(option_number==4):
        fig= px.line(data, x="Month", y="Beneficiaries", color='County')
        fig.show()
    else:
        print("Invalid Option")
        


def create_your_graph():
    #Interactive shell for utilizing create_scatterplot_counties
    print("----Welcome to the Create Your Own Graph Method---")
    print("Here are your graph options: ")
    print("1. Percent Population on Welfare over Time for a list of Counties: ")
    print("2. Adjusted Benefits Per Beneficiary over Time for a list of Counties: ")
    print("3. Adjusted Benefits Amounts over Time for a list of Counties: ")
    print("4. Beneficiaries over Time for a list of Counties: ")
    
    option=int(input("Enter Option Number: "))
    start_date=input("Enter the start point of your time period with Month spaced By Year: ")
    end_date=input("Enter the end point of your time period with Month spaced By Year: ")
    counties=[]
    county=input("Enter County Name (type q to quit)")
    while county != 'q':
        counties.append(county)
        county=input("Enter County Name (type q to quit)")
    create_scatterplot_counties(start_date,end_date,counties,option)

#Carries out create your graph
create_your_graph()
    

#Comparing Percent Population Over Time For New York City And The Rest Of New York
fig= px.line(new_data, x="time", y="Percent Population on Welfare", color='is New York')
new_data['Benefits Per Beneficiary']=(new_data["Adjusted Benefits Amounts"]/new_data["Beneficiaries"])

fig= px.line(new_data, x="time", y="Adjusted Benefits Amounts", color='is New York')
fig.show()

fig= px.line(new_data, x="time", y="Benefits Per Beneficiary", color='is New York')
fig.show()

new_data['Benefits Per Beneficiary Percent Changes']=new_data['Benefits Per Beneficiary'].pct_change()

fig= px.line(new_data, x="time", y="Benefits Per Beneficiary Percent Changes", color='is New York')
fig.show()

fig= px.line(new_data, x="time", y="Beneficiaries", color='is New York')
fig.show()


#2001 Recession

recession_2001=new_data[new_data['time']> dt.datetime(2001,2,1)]
recession_2001=recession_2001[recession_2001['time']< dt.datetime(2001,12,1)]
recession_2001["Month"]=recession_2001["Month"].replace([1,2,3,4,5,6,7,8,9,10,11,12],["Jan","Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"])
recession_2001["Month"]=[month+" "+str(year) for month,year in zip(recession_2001["Month"],recession_2001["Year"])]
recession_2001=recession_2001.sort_values('time')

recession_2001.groupby('is New York')['Percent Population on Welfare'].mean().round(2)

recession_2001.groupby('is New York')['Percent Population on Welfare'].max().round(2)

fig= px.line(recession_2001, x="Month", y="Percent Population on Welfare", color='is New York')
fig.show()


#2008 Recession

recession_2007=new_data[new_data['time']> dt.datetime(2007,11,1)]
recession_2007=recession_2007[recession_2007['time']< dt.datetime(2009,7,1)]

recession_2007.groupby('is New York')['Percent Population on Welfare'].mean().round(2)

recession_2007.groupby('is New York')['Percent Population on Welfare'].max().round(2)

fig= px.line(recession_2007, x="time", y="Percent Population on Welfare", color='is New York')
fig.show()


#Covid-19 Recession Plot

recession_2020=new_data[new_data['time']> dt.datetime(2020,1,1)]
recession_2020=recession_2020[recession_2020['time']< dt.datetime(2020,7,1)]
recession_2020["Month"]=recession_2020["Month"].replace([1,2,3,4,5,6,7,8,9,10,11,12],["Jan","Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"])
recession_2020["Month"]=[month+" "+str(year) for month,year in zip(recession_2020["Month"],recession_2020["Year"])]
recession_2020=recession_2020.sort_values('time')
recession_2020.groupby('is New York')['Percent Population on Welfare'].max().round(2)

fig= px.line(recession_2020, x="Month", y="Percent Population on Welfare", color='is New York')
fig.show()


#Covid 19 Effect on New York City Counties

recession_nyc_2020=nyc_data[nyc_data['time']> dt.datetime(2020,1,1)]
recession_nyc_2020=recession_nyc_2020[recession_nyc_2020['time']< dt.datetime(2020,7,1)]
recession_nyc_2020["Month"]=recession_nyc_2020["Month"].replace([1,2,3,4,5,6,7,8,9,10,11,12],["Jan","Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"])
recession_nyc_2020["Month"]=[month+" "+str(year) for month,year in zip(recession_nyc_2020["Month"],recession_nyc_2020["Year"])]
recession_nyc_2020=recession_nyc_2020.sort_values('time')
recession_nyc_2020.groupby('County')['Percent Population on Welfare'].mean()

fig= px.line(recession_nyc_2020, x="Month", y="Percent Population on Welfare", color='County')
fig.show()

fig= px.scatter(recession_nyc_2020, x="Month", y="Adjusted Benefits Per Beneficiary", color='County',size='Beneficiaries')
fig.show()


#The Average Percent Population on Welfare Over The Years(INACCURATE)

year_comp=data.groupby(['Year'])['Beneficiaries','Population'].sum().reset_index()
year_comp
#year_comp["Percent Population on Welfare"]=year_comp['Beneficiaries']/year_comp['Population']
#year_comp.loc[:,['Year','Percent Population on Welfare']]
