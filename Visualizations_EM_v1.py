#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("cleaned_unemployment.csv")
df.dtypes
df['FIPS Code']=df['FIPS Code'].astype(int)
df.head()

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
    
counties["features"][0]

#Build map shells
fig = px.choropleth(df, geojson=counties, locations='FIPS Code', color='Percent Population on Welfare',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa", hover_name="County",
                           labels={'Percent Population on Welfare':'Percent Population on Welfare'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(fitbounds="locations") #visible=False)
fig.show()


fig = px.choropleth(df, geojson=counties, locations='FIPS Code', color='Adjusted Benefits Per Beneficiary',
                           color_continuous_scale="Viridis",
                           range_color=(1000, 2000),
                           scope="usa", hover_name="County",
                           labels={'Adjusted Benefits Per Beneficiary':'Monthly Benefits Per Beneficiary'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(fitbounds="locations")
fig.show()

df = pd.read_csv("cleaned_unemployment.csv")

county_input = input("Please enter a county: ")

# Add data
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
         'August', 'September', 'October', 'November', 'December']

df_input = df[df["County"]==county_input]

df_2001 = df_input[(df_input['Year']==2001)]

df_2008 = df_input[(df_input['Year']==2008)]

df_2020 = df_input[(df_input['Year']==2020)]

fig = go.Figure()

# Create and style traces
fig.add_trace(go.Scatter(x=month, y=df_2001["Beneficiaries"], name='# of Beneficiaries in 2001',
                         line=dict(color='firebrick', width=4,dash='dash')))
fig.add_trace(go.Scatter(x=month, y=df_2008["Beneficiaries"], name='# of Beneficiaries in 2008',
                         line=dict(color='royalblue', width=4, dash='dot')))
fig.add_trace(go.Scatter(x=month, y=df_2020["Beneficiaries"], name='# of Beneficiaries in 2020',
                         line=dict(color='green', width=4)))

fig.update_layout(title='Number of Unemployment Beneficiaries for Each Recession in the 2000s in '+county_input+' County',
                   xaxis_title='Month',
                   yaxis_title='# of Beneficiaries')
