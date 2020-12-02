import pandas as pd
import numpy as np
import zipfile
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json

usda_zip = zipfile.ZipFile('data/FoodEnvironmentAtlas.zip')
varlist = pd.read_csv(usda_zip.open('VariableList.csv'))
df = pd.read_csv(usda_zip.open('StateAndCountyData.csv'))

sheets = ['ACCESS', 'STORES', 'RESTAURANTS', 'ASSISTANCE', 'INSECURITY', 'TAXES', 'LOCAL', 'HEALTH', 'SOCIOECONOMIC']
for sheet in sheets:

access = pd.read_excel('data/FoodEnvironmentAtlas.xls', sheet_name='ACCESS')
stores = pd.read_excel('data/FoodEnvironmentAtlas.xls', sheet_name='STORES')
restaurants = pd.read_excel('data/FoodEnvironmentAtlas.xls', sheet_name='RESTAURANTS')
assistance = pd.read_excel('data/FoodEnvironmentAtlas.xls', sheet_name='ASSISTANCE')
insecurity = pd.read_excel('data/FoodEnvironmentAtlas.xls', sheet_name='INSECURITY')
taxes = pd.read_excel('data/FoodEnvironmentAtlas.xls', sheet_name='TAXES')
local = pd.read_excel('data/FoodEnvironmentAtlas.xls', sheet_name='LOCAL')
health = pd.read_excel('data/FoodEnvironmentAtlas.xls', sheet_name='HEALTH')
socioeconomic = pd.read_excel('data/FoodEnvironmentAtlas.xls', sheet_name='SOCIOECONOMIC')
county = pd.read_excel('data/FoodEnvironmentAtlas.xls', sheet_name='Supplemental Data - County')

local.drop(3143, 'index', inplace=True)

#Selecting relevant columns
df1 = access[['FIPS', 'State', 'County', 'LACCESS_POP15', 'PCT_LACCESS_POP15']].copy()
df2 = stores[['FIPS', 'GROC16', 'SUPERC16', 'CONVS16', 'SPECS16']].copy()
df3 = restaurants[['FIPS', 'FFR16', 'FSR16', 'PC_FFRSALES12', 'PC_FSRSALES12']].copy()
df4 = assistance[['FIPS', 'PCT_SNAP12', 'PCT_NSLP12', 'PCT_WIC12', 'PCH_FDPIR_12_15', 'FOOD_BANKS18']].copy()
df5 = taxes[['FIPS', 'SODATAX_STORES14', 'CHIPSTAX_STORES14', 'FOOD_TAX14']].copy()
df6 = local[['FIPS', 'DIRSALES_FARMS12', 'FMRKT13', 'VEG_FARMS12']].copy()
df7 = socioeconomic[['FIPS', 'PCT_NHWHITE10', 'PCT_NHBLACK10', 'PCT_HISP10', 'PCT_NHASIAN10', 'PCT_NHNA10', 'PCT_NHPI10', 'PCT_65OLDER10', 'PCT_18YOUNGER10', 'MEDHHINC15', 'POVRATE15']].copy()
df8 = county[['FIPS', 'Population_Estimate_2015']].copy()

dfs = [df1, df2, df3, df4, df5, df6, df7, df8]
for df in dfs:
    df.set_index('FIPS', inplace=True)
food_access = pd.concat(dfs, axis=1)

food_access = food_access[food_access['State'].notna()]

col_names_old = food_access.columns
column_names = ['state', 'county',
                'low_access','pct_low_access',
                'stores_grocery', 'stores_club', 'stores_conv', 'stores_special',
                'fast_food', 'restaurants',
                'exp_fast_food_percap', 'exp_restaurants_percap',
                'snap_participants', 'nat_school_lunch_participants', 'wic_participants',
                'fdpir_sites', 'food_banks',
                'soda_tax', 'chip_tax', 'food_tax',
                'farms_direct_sales', 'farmers_markets', 'veg_farms',
                'white', 'black', 'hisp', 'asian', 'native', 'pacific_islander',
                'older_65', 'younger_18',
                'median_income', 'poverty_rate',
                'population']

new_col_dict = {}
for old, new in zip(col_names_old, column_names):
    new_col_dict[old] = new

food_access.rename(columns=new_col_dict)

food_access.to_csv('data/food_access.csv')