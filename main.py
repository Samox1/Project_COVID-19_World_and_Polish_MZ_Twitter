# This is project:
# Project_COVID-19_World_and_Polish_MZ_Twitter
# Author: Szymon Baczyński
# Start date: 10 / 2020
# Target: Build Python script where data about COVID-19 will be processed and visualize
# To Do List:
#       1) Visualization for Global data:
#           1.1) Download data from GitHub: https://github.com/CSSEGISandData/COVID-19
#               1.1.1) Vis for: time_series_covid19_confirmed_global.csv = https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
#       2) Visualization for data from Poland - Twitter = Ministry of Health (Poland)
#           2.1) Scraping Twitter: https://twitter.com/MZ_GOV_PL
#               2.1.1) Vis deaths from Twitter (scrap + regex)
#                   2.1.1.1) Scrap Twitter: GetOldTweets3 : https://towardsdatascience.com/how-to-scrape-tweets-from-twitter-59287e20f0f1

import psutil
import pandas as pd
import datetime
import numpy as np
import math
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly.offline as py
import plotly
import bokeh
import folium

# Functions Part ------------------------------------------------------------------------------------ #
def import_GitHub_time_series_covid19_confirmed_global():
    """
    Import COVID19 data "time_series_covid19_confirmed_global.csv" from GitHub = CSSEGISandData

    :return: DataFrame
    """
    print("Function: import_GitHub_time_series_covid19_confirmed_global")
    file_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    confirmed_global = pd.read_csv(file_url)
    print(confirmed_global.head(10))
    return confirmed_global


def choose_country_to_plot(import_data, country):
    """
    Function to export data for specific country or list of country.

    :param import_data: DataFrame with imported data about COVID-19
    :param country: string or list with country to find data
    :return: pandas DataFrame
    """
    print("Function: choose_country_to_plot")
    # for i in country:
        # print(country)

    df = pd.DataFrame()
    df['date'] = import_data.columns



    for i in country:
        if len(import_data[import_data['Country/Region'] == i]) > 1:
            more_regions = import_data[import_data['Country/Region'] == i]
            # print(more_regions)
            reg_name = [name for name in more_regions["Province/State"]]
            # print(reg_name)

            for ii, i_reg in enumerate(reg_name):
                if str(i_reg) == "nan":
                    # print(ii)
                    # print(i_reg)
                    df[i] = (more_regions.iloc[ii, :]).to_numpy().T
                else:
                    #print(i + ": " + str(i_reg))
                    col_name = i + ": " + str(i_reg)
                    df[col_name] = (more_regions[more_regions["Province/State"] == i_reg]).to_numpy().T
        else:
            df[i] = (import_data[import_data['Country/Region'] == i]).to_numpy().T

    # print(df)
    df = df[4:]
    df['date'] = pd.to_datetime(df["date"]).dt.strftime('%d-%m-%Y')

    return df


# Functions Part ------------------------------------------------------------------------------------ #


confirmed_global = import_GitHub_time_series_covid19_confirmed_global()
df = choose_country_to_plot(confirmed_global, ["Poland", "Sweden", "France", "Germany"])
print(df)

fig = px.line(df, x='date', y=df.columns )
fig.update_xaxes(rangeslider_visible=True)
fig.show()
fig.write_html('COVID19_Confirmed.html')


# Daily Part

confirmed_daily = df

for columns_name in confirmed_daily.columns:
    if columns_name != 'date':
        confirmed_daily.loc[:,columns_name] = confirmed_daily.loc[:,columns_name].diff(1)

fig = px.line(confirmed_daily, x='date', y=confirmed_daily.columns)
#fig.update_xaxes(rangeslider_visible=True)
fig.show()
fig.write_html('COVID19_Confirmed_Daily.html')

print(confirmed_daily)


# Map Part = https://python-graph-gallery.com/313-bubble-map-with-folium/

# Plotly Map = https://github.com/Mythili7/Choropleth/blob/master/Choropleth%20map%20using%20global%20COVID-19%20data.ipynb
# HeatMap = COVID19 Dataset = https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv

dataset_url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
df = pd.read_csv(dataset_url)

fig = px.choropleth(df, locations = 'Country', locationmode = 'country names', color = 'Confirmed'
                    ,animation_frame = 'Date')
fig.update_layout(title_text = 'Global spread of Covid19')
# fig.show()
py.offline.plot(fig, filename='Plotly_Global_covid.html')


# Look there = https://towardsdatascience.com/spread-of-covid-19-with-interactive-data-visualization-521ac471226e
