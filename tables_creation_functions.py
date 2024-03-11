import pandas as pd
import time


def create_dataframe(url: str):
    """
    Creates a dataframe with each team stats from season stats on fbref.

    Args:
     - url (str): fbref season url

    Returns:
     - df (pandas.DataFrame) : Dataframe with stats
    """

    df0 = pd.read_html(url)

    main = df0[0][[
        'Squad',
        'MP',
        'Pts/MP']]

    goalkeeping = df0[4][[
        ('Unnamed: 0_level_0',    'Squad'),
        ('Performance',    'GA'),
        ('Performance',    'Save%')]]
    goalkeeping.columns = goalkeeping.columns.get_level_values(1)

    shooting = df0[8][[
        ('Unnamed: 0_level_0',    'Squad'),
        ('Standard',    'Gls'),
        ('Standard',    'Sh/90'),
        ('Standard',    'Dist'),
        ('Standard',    'PKatt')]]
    shooting.columns = shooting.columns.get_level_values(1)

    passing = df0[10][[
        ('Unnamed: 0_level_0',    'Squad'),
        ('Unnamed: 17_level_0',     'Ast'),
        ('Total',    'Cmp'),
        ('Total',    'Cmp%'),
        ('Total',    'PrgDist')]]
    passing.columns = passing.columns.get_level_values(1)

    defensive_actions = df0[16][[
        ('Unnamed: 0_level_0',    'Squad'),
        ('Unnamed: 16_level_0', 'Tkl+Int'),
        ('Unnamed: 18_level_0',     'Err')]]
    defensive_actions.columns = defensive_actions.columns.get_level_values(1)

    posession = df0[18][[
        ('Unnamed: 0_level_0',    'Squad'),
        ('Touches',    'Att 3rd'),
        ('Carries',    'TotDist')]]
    posession.columns = posession.columns.get_level_values(1)

    miscellaneous__stats = df0[22][[
        ('Unnamed: 0_level_0',    'Squad'),
        ('Performance',    'Fls'),
        ('Aerial Duels',    'Won%')]]
    miscellaneous__stats.columns = miscellaneous__stats.columns.get_level_values(1)

    df = pd.concat([main.set_index('Squad'),
                    goalkeeping.set_index('Squad'),
                    shooting.set_index('Squad'),
                    passing.set_index('Squad'),
                    defensive_actions.set_index('Squad'),
                    posession.set_index('Squad'),
                    miscellaneous__stats.set_index('Squad')], axis=1, join='outer').reset_index().rename(columns={'index': 'Squad'})

    new_columns = [
        'Gls',
        'GA',
        'Ast',
        'PKatt',
        'Cmp',
        'PrgDist',
        'Tkl+Int',
        'Err',
        'Att 3rd',
        'TotDist',
        'Fls'
    ]

    for element in new_columns:
        df[element] = df[element] / df['MP']

    df = df.drop(['Squad', 'MP'], axis=1)

    # rearange dataframe for more comfort
    df = df[['Pts/MP', 'Gls', 'GA', 'Ast',
             'Sh/90', 'Dist', 'PKatt',
             'Cmp', 'Cmp%', 'PrgDist',
             'Att 3rd', 'TotDist',
             'Tkl+Int', 'Err', 'Save%',
             'Fls', 'Won%']]

    return df


def generate_urls(league=None) -> list:
    """
    Creates a list of fbref Top-5 leagues urls.

    Returns:
    urls (list) : List of fbref urls of Top 5 leagues, last 6 years
    """

    initial_year = 2023
    year_span = 6

    epl_start = 'https://fbref.com/en/comps/9/'
    epl_end = '-Premier-League-Stats'

    laliga_start = 'https://fbref.com/en/comps/12/'
    laliga_end = '-La-Liga-Stats'

    serie_a_start = 'https://fbref.com/en/comps/11/'
    serie_a_end = '-Serie-A-Stats'

    bundesliga_start = 'https://fbref.com/en/comps/20/'
    bundesliga_end = '-Bundesliga-Stats'

    league1_start = 'https://fbref.com/en/comps/13/'
    league1_end = '-Ligue-1-Stats'

    leagues = [(epl_start, epl_end),
               (laliga_start, laliga_end),
               (serie_a_start, serie_a_end),
               (bundesliga_start, bundesliga_end),
               (league1_start, league1_end)]

    years = [i for i in range(initial_year - year_span, initial_year + 1)]
    urls = []

    for start, end in leagues:
        for i in range(len(years)-1):
            year_str = str(years[i]) + '-' + str(years[i + 1])
            urls.append(start + year_str + '/' + year_str + end)

    return urls


# creating a dataset, top 5 leagues, 6 last years
urls = generate_urls()
leagues = []

for el in urls:
    time.sleep(1)
    leagues.append(create_dataframe(el))

df = pd.concat(leagues, ignore_index=True)
df.to_csv('./data/top5_leagues_data.csv', index=False)


# creating a current prem table
prem_url = 'https://fbref.com/en/comps/9/Premier-League-Stats'
prem_df = create_dataframe(prem_url)
prem_df.to_csv('./data/epl_07_03.csv', index=False)
