import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, date, timedelta
import pytz  # for timezone conversion

# SETTINGS

pd.set_option('display.expand_frame_repr', False)
pd.set_option("display.max_rows", 50000, "display.max_columns", 500)
pd.set_option('display.expand_frame_repr', False)
pd.options.mode.chained_assignment = None

URL = "https://finance.yahoo.com/u/yahoo-finance/watchlists/most-active-penny-stocks"

# MAIN

page = requests.get(URL, headers={'User-Agent': 'Custom'})
soup = BeautifulSoup(page.content, "html.parser")
tables = soup.find_all('table')
table = soup.find('table', class_='cwl-symbols W(100%)') # table name, change as needed
column_names = [ele.text.strip() for ele in table.find_all('th')]

# Define an empty dataframe
df = pd.DataFrame(columns=column_names)

# Collect data
for row in table.tbody.find_all('tr'):

    # Find all data for each column
    columns = row.find_all('td')

    if columns:  # Check if we have data
        # Collect data for each column
        data = [ele.text.strip() for ele in columns]
        df = pd.concat([df, pd.DataFrame([data], columns=column_names)], ignore_index=True)

# Drop and filter the bullshit
df = df.loc[df['Change'] != '-']
df = df.loc[df['% Change'] != '-']
df['Change'] = df['Change'].str.replace('+', '', regex=False)
df['Change'] = df['Change'].astype(float)
df = df.loc[df['Change'] > 0.1]

# Add date as index
date_today = datetime.now(pytz.timezone('America/New_York')).date()
df['Date'] = date_today
df.set_index('Date', inplace=True)
