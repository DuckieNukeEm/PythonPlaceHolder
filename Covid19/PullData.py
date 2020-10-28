import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date

MAIN_DATA = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
US_DATA = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/"


def pull_daily_data(URL: str = MAIN_DATA,
                    start_dt: str = '01-22-2020',
                    end_dt: str = None,
                    verbose: bool = False) -> pd.DataFrame:
    start_date = datetime.strptime(start_dt, '%m-%d-%Y').date()
    Cur_date = start_date
    if end_dt is None:
        end_dt = datetime.date(datetime.today())
    else:
        end_dt = datetime.strptime(end_dt, '%d-%m-%Y')

    data_dict = dict()
    while Cur_date <= end_dt:
        if verbose:
            print('Working on date: {}'.format(Cur_date.strftime("%Y-%m-%d")))
        try:
            df_temp = pd.read_csv(URL + Cur_date.strftime("%m-%d-%Y") + '.csv')
            df_temp['date'] = Cur_date.strftime("%Y-%m-%d")
            df_temp = df_temp.rename(columns={"Province/State": "State",
                                            "Country/Region": "Country",
                                            'Province_State': 'State',
                                            'Country_Region': "Country",
                                            'Latitude': 'Lat',
                                            'Longitude': "Long",
                                            'Long_': 'Long',
                                            'Last Update': 'Last_Update'})
            data_dict[Cur_date.strftime("%Y-%m-%d")] = df_temp
        except Exception:
            print('skiping')
        Cur_date = Cur_date + timedelta(days=1)

    df = pd.concat([v for v in data_dict.values()], ignore_index=True)

    return(df)


def pull_data(start_dt: str = '01-22-2020',
            end_dt: str = None,
            URL: str = MAIN_DATA,
            US_URL: str = US_DATA,
            switch_USA: bool = False) -> pd.DataFrame:
    print("Pulling all data")
    df = pull_daily_data(URL=URL,
                        start_dt=start_dt,
                        end_dt=end_dt)

    if switch_USA is False:
        print("Returning Data")
        return(df)

    if datetime.strptime(start_dt, '%m-%d-%Y').date() < date(2020, 4, 12):
        start_dt = '04-12-2020'

    print("Pulling US Data")
    df_us = pull_daily_data(URL=US_URL,
                            start_dt=start_dt, 
                            end_dt=end_dt)
    df_us = df_us \
                .assign(Combined_Key=lambda x: x.State + ', US')
    US_Cols_to_keep = [x for x in df_us.columns if x in df.columns]

    print("merging Data")
    df_us = df_us[US_Cols_to_keep]
    df_us = df_us[df_us.State != 'Recovered']
    
    df = df[~((df.Country == 'US') &
            (pd.to_datetime(df.date) > datetime(2020, 4, 11)))]
    df = pd.concat([df, df_us])

    df.reset_index()
    return(df)


def fix_locals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Fixing USA
    Ind_2_State = {
            'D.C.': 'District of Columbia',
            'AL': 'Alabama',
            'AK': 'Alaska',
            'AZ': 'Arizona',
            'AR': 'Arkansas',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DE': 'Delaware',
            'DC': 'District of Columbia',
            'FL': 'Florida',
            'GA': 'Georgia',
            'HI': 'Hawaii',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'IA': 'Iowa',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'ME': 'Maine',
            'MD': 'Maryland',
            'MA': 'Massachusetts',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MS': 'Mississippi',
            'MO': 'Missouri',
            'MT': 'Montana',
            'NE': 'Nebraska',
            'NV': 'Nevada',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NY': 'New York',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VT': 'Vermont',
            'VA': 'Virginia',
            'WA': 'Washington',
            'WV': 'West Virginia',
            'WI': 'Wisconsin',
            'WY': 'Wyoming',
            'PR': 'Puerto Rico',
            'Unassigned Location (From Diamond Princess)': 'Diamond Princess',
            'Grand Princess Cruise Ship': 'Grand Princess',
            'CA (From Diamond Princess)': 'Diamon Princess',
            'United States Virgin Islands': 'Virgin Islands',
            'TX (From Diamond Princess)': 'Diamond Princess',
            'NE (From Diamond Princess)': 'Diamond Princess',
            'Chicago': 'Illinois'}
    df = df \
        .assign(State_Fix_1=lambda x: x.State
                                    .str
                                    .split(', ')
                                    .str[-1]
                                    .str
                                    .strip()
                                    .map(Ind_2_State, 'ignore'),
                State=lambda x: np.where((x.Country == 'US'),
                                        np.where(x.State_Fix_1.isna(),
                                                x.State,
                                                x.State_Fix_1),
                                        x.State)) \
        .drop(columns=['State_Fix_1'])

    country_dict = {'Diamond Princess': 'Boats',
                    'Grand Princess': 'Boats',
                    'Northern Mariana Islands': 'US Other',
                    'Virgin Islands': 'US Other',
                    'Virgin Islands, U.S.': 'US Other',
                    'Guam': 'US Other',
                    'Puerto Rico': 'US Other',
                    'American Samoa': 'US Other',
                    'Recovered': 'US'}
    df = df \
        .assign(C1=lambda x: x.State.map(country_dict, 'ignore'),
                Country=lambda x: np.where(x.C1.isna(), x.Country, x.C1),
                State=lambda x: np.where(x.State.isna(), '-', x.State)) \
        .drop(columns={'C1'}) \
        .assign(Country=lambda x: np.where(x.Combined_Key == 'Recovered, Canada',
                                        'Canada',
                                        x.Country))

    return(df)


def calc_daily(df: pd.DataFrame, Level: list) -> pd.DataFrame:
    """calculates the current active via the following formula
    DailyRecovered = Recovered - Recovered[-1],
    DailyDeaths = Deaths - Deaths[-1]
    DailyActive = Confirmed - Active - Deaths
    NetChange = Active - Active[1]
    """

    if 'date' not in Level:
        Level_with_Date = Level + ['date']
    else:
        Level_with_Date = Level
        Level = [x for x in Level if x != 'date']

    df_group = df.fillna(0) \
                .assign(Active=lambda x: np.where((x.Active == 0) |
                                                (x.Active == (x.Confirmed -
                                                                x.Deaths)),
                                                x.Confirmed -
                                                x.Deaths -
                                                x.Recovered,
                                                np.where((x.State == 'Recovered') &
                                                            (x.Active != x.Recovered*-1),
                                                            x.Recovered * -1,
                                                            x.Active)),
                        )\
                .groupby(Level_with_Date)\
                [['Active', 'Confirmed', 'Deaths', 'Recovered']] \
                .sum() \
                .reset_index()

    df_group = pd.concat([df_group,
                        df_group \
                            .groupby(Level)
                            [['Active', 'Confirmed', 'Deaths', 'Recovered']] \
                            .shift() \
                            .rename(columns={'Active': 'Active_L1', 
                                            'Confirmed': 'Confirmed_L1',
                                            'Deaths': 'Deaths_L1',
                                            'Recovered': 'Recovered_L1'}) \
                            .fillna(0)
                        ],
                        axis=1)
    df_group = df_group \
                .assign(Recovered_Daily=lambda x: x.Recovered - x.Recovered_L1,
                        Deaths_Daily=lambda x: x.Deaths - x.Deaths_L1,
                        NewCases_Daily=lambda x: x.Confirmed - x.Confirmed_L1,
                        Active_Daily=lambda x: x.Confirmed - x.Deaths - x.Recovered,
                        NetChange=lambda x: x.NewCases_Daily -
                                            x.Recovered_Daily -
                                            x.Deaths_Daily,
                        Error=lambda x: x.Active_L1 - x.Active + x.NetChange
                        ) \
                .drop(columns=['Active_L1', 'Confirmed_L1', 'Deaths_L1', 'Recovered_L1']) 

    return(df_group)


def get_data(URL: str = MAIN_DATA,
            US_URL: str = US_DATA,
            Level: list = ['Country'],
            switch_USA: bool = False,
            start_dt: str = '01-22-2020',
            end_dt: str = None) -> pd.DataFrame:
    """Pulls data and cleans it for you too
    """
    df = pull_data(start_dt=start_dt,
                end_dt=end_dt,
                URL=URL,
                US_URL=US_URL,
                switch_USA=switch_USA)
    df = fix_locals(df)
    df = calc_daily(df, Level=Level)

    return(df)

def get_pop(fips_loc: str = "./Data/fips_to_county.csv",
            county_pop:str = './Data/co-est2019-alldata.csv',
            country_pop= ''):
    # merging fips with county populations
    Df_fips = pd.read_csv(fips_loc)
    Df_fips['fipscounty'] = Df_fips.fipscounty.apply(lambda x: 44990 if x == 44999 else x)
    Df_fips['fipscounty'] = Df_fips.fipscounty.apply(lambda x: x if x != 46113 else 46102)
    Df_fips['fipscounty'] = Df_fips.fipscounty.apply(lambda x: x if x !=  2270 else  2158)
    # Loading County/State level  population information
    Df_state = pd.read_csv(county_pop, encoding = 'latin-1')\
                        .rename(columns = {'POPESTIMATE2010':'pop',
                                           'STATE':'state',
                                            'COUNTY':'county'})
    Df_state['county'] = Df_state.county.apply(lambda x: x if x > 0 else 990)

    Df_state = Df_state.assign(fipscounty = lambda x: x.state * 1000 + x.county)
        
    #Df_state = Df_state[['fipscounty','pop','state','county']]
    Fips_pop = ppd.merge(
                              Df_fips,
                              Df_state[['fipscounty','pop']],
                              how = 'inner',
                              on = ['fipscounty'])\
                    .assign(pop_100k = lambda x: round(x['pop']/100000,2))\
                    .rename(columns = {'fipsstate':'state_cd',
                                       'fipscounty':'FIPS'}) \
                    .drop(columns = ['ssastate','ssacounty'])


    #Loading world level infom
    Df_wrld = pd.read_csv('./Data/WorldPopulation.csv') \
                .query("Type == 'Country/Area'")\
                .rename(columns = {'2020':'pop'})\
                [['Country','Country code','pop']]\
                .assign(pop_100k = lambda x: round(x['pop']/100000,2))
    
    return(Fips_pop, Df_wrld)

if False:  
    df = pull_data(switch_USA=True)
    df_fix = fix_locals(df)
    df_day = calc_daily(df_fix, ['Country'])

    DATE = datetime.today() + timedelta(days=-4)
    DATE = DATE.strftime('%Y-%m-%d')
    df_day.query('Country in ["US","Italy"] and date >= @DATE')


    df_day.query('Country == "US"').to_csv('/home/asmodi/Downloads/USA_Covid.csv', index=False)

    df_day.query('Country == "Italy"').to_csv('/home/asmodi/Downloads/Italy_Covid.csv', index=False)
    df_day.query('Country == "Italy" and date >= @DATE')

if False:
    df_day = get_data(Level = ['Country'], switch_USA = True)

    DATE = datetime.today() + timedelta(days=-4)
    DATE = DATE.strftime('%Y-%m-%d')
    df_day.query('Country in ["US","Italy"] and date >= @DATE')