#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:52:50 2020

@author: ben_cosgo
"""


# libraries
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_style("white")
import pandas as pd
import plotly.express as px
my_dpi=96
 
# Get the data. Filepath may differ
data = pd.read_csv("cleaned_unemployment.csv")

import datetime as dt

dt.datetime.strptime("2020 1", '%Y %m')


data['time']=[dt.datetime.strptime(str(year)+' ' + str(month), '%Y %m') for year,month in zip(data['Year'],data['Month'])]

data= data.sort_values(['time'])
data=data.groupby(['Region',"time","Month","Year"])['Adjusted Benefits Amounts','Population','Beneficiaries'].sum()
data=data.round(2)
data=data.reset_index()

data['Adjusted Benefits Per Beneficiary']=data['Adjusted Benefits Amounts']/data['Beneficiaries']
data['Percent Population on Welfare']=(data['Beneficiaries']/data['Population'])*100
data["Month"]=data["Month"].replace([1,2,3,4,5,6,7,8,9,10,11,12],["Jan","Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"])
data["Month"]=[month+" "+str(year) for month,year in zip(data["Month"],data["Year"])]
data=data.sort_values('time').round(2)


# And I need to transform my categorical column (continent) in a numerical value group1->1, group2->2...
#data['Region']=pd.Categorical(data['Region'])

#Needs fitting with datetime
# For each year:
data=data[data["time"]<=dt.datetime(2020,2,1)]
for i in sorted(data["time"].unique()):

# initialize a figure
    #fig = plt.figure(figsize=(680/my_dpi, 480/my_dpi), dpi=my_dpi)
# Change color with c and alpha. I map the color to the X axis value.
    tmp=data[ data["time"] == i ]
    tmp=tmp.sort_values("Region")
    #print(type(i))
    #sns.relplot(x='Percent Population on Welfare',y='Adjusted Benefits Per Beneficiary',hue='Region',size=tmp["Population"],alpha=0.6,data=tmp,palette='Set2',sizes=(200,2000),height=7)
    #plt.scatter(tmp['Percent Population on Welfare'], tmp['Adjusted Benefits Per Beneficiary'] , s=tmp['Population']/1000 , c=tmp['Region'].cat.codes, cmap="Accent", alpha=0.6, edgecolors="white", linewidth=2)
    #plt.annotate(tmp[tmp["Region"]=="Capital"]["Region"][0],(tmp[tmp["Region"]=="Capital"]['Percent Population on Welfare'][0],tmp[tmp["Region"]=="Capital"]['Adjusted Benefits Per Beneficiary'][0]))
# Add titles (main and on axis)
#plt.yscale('log')
  
    the_title= str(tmp["Month"].unique()[0])
    #plt.xlabel("Percent Population on Welfare")
    # plt.ylabel("Adjusted Benefits Per Beneficiary")
    # plt.title(the_title)
    # plt.ylim(200,2000)
    # plt.xlim(0, 12)
    
    
    fig= px.scatter(tmp, x="Percent Population on Welfare", y="Adjusted Benefits Per Beneficiary", color='Region',size='Population',size_max=50,title=the_title,color_discrete_sequence=px.colors.qualitative.Dark24)
    fig.update_yaxes(range=[200,2000])
    fig.update_xaxes(range=[0, 4])
    fig.update_traces(marker=dict(opacity=0.5))
    #plt.legend(tmp['Region'].cat.codes,tmp['Region'])

# Save it
    filename='Unemployment attempt'+str(i)+'.png'
    fig.write_image(filename)
    # plt.savefig(filename, dpi=96)
    # plt.gca()


#Then use image magick (this is bash, not python)
#convert -delay 20 Unemployment*.png animated_gapminder.gif


