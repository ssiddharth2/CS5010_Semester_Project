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
my_dpi=96
 
# Get the data. Filepath may differ
data = pd.read_csv("/Users/ben_cosgo/Learning_Python/CS5010_Semester_Project/CS5010_Semester_Project/cleaned_unemployment.csv")

# And I need to transform my categorical column (continent) in a numerical value group1->1, group2->2...
data['Region']=pd.Categorical(data['Region'])
'''
#Needs fitting with datetime
# For each year:
for i in data.year.unique():

# initialize a figure
fig = plt.figure(figsize=(680/my_dpi, 480/my_dpi), dpi=my_dpi)
 
# Change color with c and alpha. I map the color to the X axis value.
tmp=data[ data.year == i ]
'''
plt.scatter(tmp['Percent Population on Welfare'], tmp['Adjusted Benefits Per Beneficiary'] , s=tmp['Population']/1000 , c=tmp['Region'].cat.codes, cmap="Accent", alpha=0.6, edgecolors="white", linewidth=2)
 
# Add titles (main and on axis)
#plt.yscale('log')
plt.xlabel("Percent Population on Welfare")
plt.ylabel("Adjusted Benefits Per Beneficiary")
plt.title("Year: "+str(i) )
plt.ylim(200,2000)
plt.xlim(0, 12)

# Save it
filename='Unemployment Visualization'+str(i)+'.png'
plt.savefig(filename, dpi=96)
plt.gca()

'''
# Then use image magick (this is bash, not python)
convert -delay 80 Gapminder*.png animated_gapminder.gif
'''

