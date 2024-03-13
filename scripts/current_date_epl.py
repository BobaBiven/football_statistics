from tables_creation_functions import create_dataframe, generate_urls
from datetime import datetime
import time
import pandas as pd

"""
This script exists solely to generate a datasets
"""

# creating a dataset, top 5 leagues, 6 last years
urls = generate_urls()
leagues = []

for el in urls:
    time.sleep(1)
    leagues.append(create_dataframe(el))

df = pd.concat(leagues, ignore_index=True)
df.to_csv('../data/historical_stats.csv', index=False)


# epl 07.03.2023
current_date = datetime.today().strftime('%Y-%m-%d')
file_name = f'../data/epl_{current_date}.csv'
prem_url = 'https://fbref.com/en/comps/9/Premier-League-Stats'
prem_df = create_dataframe(prem_url)
prem_df.to_csv(file_name, index=False)
