# libraries
import datetime as dt
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_style("white")
my_dpi = 96

# Get the data. Filepath may differ
data = pd.read_csv("cleaned_unemployment.csv")


dt.datetime.strptime("2020 1", '%Y %m')

# Create date time version for each row that will be used for sorting by time
data['time'] = [dt.datetime.strptime(str(year)+' ' + str(month), '%Y %m')
                for year, month in zip(data['Year'], data['Month'])]

# Aggreggate the region and take the sums of the Population, Benefit amounts, and Beneficiaries for each column
data = data.sort_values(['time'])
data = data.groupby(['Region', "time", "Month", "Year"])[
    'Adjusted Benefits Amounts', 'Population', 'Beneficiaries'].sum()
data = data.round(2)
data = data.reset_index()

# Recalculate The Adjusted Benefits Per Beneficiary and Percent Population on Welfate
data['Adjusted Benefits Per Beneficiary'] = data['Adjusted Benefits Amounts'] / \
    data['Beneficiaries']
data['Percent Population on Welfare'] = (
    data['Beneficiaries']/data['Population'])*100
data["Month"] = data["Month"].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [
                                      "Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"])
data["Month"] = [month+" "+str(year)
                 for month, year in zip(data["Month"], data["Year"])]
data = data.sort_values('time').round(2)


# Filter the data so that data frame only the pre-COVID dates
data = data[data["time"] <= dt.datetime(2020, 2, 1)]

# Loop through each date in the dataframe to create scatterplot for the respective time period
for i in sorted(data["time"].unique()):

    # Filter the data based on the time
    tmp = data[data["time"] == i]
    tmp = tmp.sort_values("Region")

    # title based on month and year
    the_title = str(tmp["Month"].unique()[0])

    # Create scatterplot
    fig = px.scatter(tmp, x="Percent Population on Welfare", y="Adjusted Benefits Per Beneficiary", color='Region',
                     size='Population', size_max=50, title=the_title, color_discrete_sequence=px.colors.qualitative.Dark24)
    fig.update_yaxes(range=[200, 2000])
    fig.update_xaxes(range=[0, 4])
    fig.update_traces(marker=dict(opacity=0.5))

    # Save scatterplot
    filename = 'Unemployment attempt'+str(i)+'.png'
    fig.write_image(filename)


# Then use image magick (this is bash, not python)
# convert -delay 20 Unemployment*.png animated_gapminder.gif
