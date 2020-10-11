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
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly
import bokeh
import folium

# Functions Part ------------------------------------------------------------------------------------ #
def import_time_series_covid19_confirmed_global_GitHub():
    """
    Import COVID19 data "time_series_covid19_confirmed_global.csv" from GitHub = CSSEGISandData

    :return: DataFrame
    """
    print("Function: import_COVID19_GitHub")
    file_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    confirmed_global = pd.read_csv(file_url)
    print(confirmed_global.head(10))
    return confirmed_global


# Functions Part ------------------------------------------------------------------------------------ #

# Download file with COVID-19 Data = refresh every day
#file_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
#confirmed_global_file = wget.download(file_url, "time_series_covid19_confirmed_global.csv")

# Import Confirmed Data
#confirmed_global = pd.read_csv(file_url)
#print(confirmed_global.head(10))


confirmed_global = import_time_series_covid19_confirmed_global_GitHub()

print(confirmed_global[confirmed_global['Country/Region'] == 'Poland'])
confirmed_Poland = confirmed_global[confirmed_global['Country/Region'] == 'Poland']
print(confirmed_Poland)


df = pd.DataFrame()
df['date'] = confirmed_global.columns[4:]
df['Poland'] = (confirmed_Poland.to_numpy().T)[4:]

fig = px.line(df, x='date', y=df.columns)
fig.update_xaxes(rangeslider_visible=True)
fig.show()
fig.write_html('PL_confirmed.html')
