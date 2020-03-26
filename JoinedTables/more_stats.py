import pandas as pd

dfc = pd.read_csv('BedsToCovidByCounty.csv')
dfs = pd.read_csv('BedsToCovidByState.csv')

dfc['Normalized Beds'] = dfc['Hospital Beds']/dfc['Total Population']
dfc['Normalized ICU Beds'] = dfc['ICU Beds']/dfc['Total Population']
dfc['Normalized Cases'] = dfc['Confirmed Cases']/dfc['Total Population']
dfc['Normalized Deaths'] = dfc['Deaths']/dfc['Total Population']
dfc['Normalized Deaths 60+'] = dfc['Deaths']/dfc['Population Aged 60+']

dfc.to_csv('BedsToCovidByCounty.csv')

dfs['Normalized Beds'] = dfs['Hospital Beds']/dfs['Total Population']
dfs['Normalized ICU Beds'] = dfs['ICU Beds']/dfs['Total Population']
dfs['Normalized Cases'] = dfs['Confirmed Cases']/dfs['Total Population']
dfs['Normalized Deaths'] = dfs['Deaths']/dfs['Total Population']
dfs['Normalized Deaths 60+'] = dfs['Deaths']/dfs['Population Aged 60+']


dfs.to_csv('BedsToCovidByState.csv')
