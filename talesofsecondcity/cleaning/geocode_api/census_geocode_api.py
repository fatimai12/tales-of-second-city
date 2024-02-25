"""
CAPP 30122
Team: Tales of Second City
Author: Victoria Beck

Use Census Geocode API to match zipcodes to census tracts

Code based on https://github.com/greennumbers/python/blob/main/PYTHON_CENSUS_API.ipynb

"""
import requests
import pandas as pd
import io
import csv

url = 'https://geocoding.geo.census.gov/geocoder/geographies/addressbatch'
files = {'address_file': ('C:\TEMP\ADDRESS_SAMPLE.csv', 
                          open('C:\TEMP\ADDRESS_SAMPLE.csv', 'rb'), 'text/csv')}
payload = {'benchmark':'Public_AR_Current','vintage':'Current_Current'}
s = requests.post(url, files=files, data=payload)

df = pd.read_csv(io.StringIO(s.text), sep=',', header=None, quoting=csv.QUOTE_ALL)
df.columns = ['ID', 'ADDRESS_IN', 'MATCH_INDICATOR', 'MATCH_TYPE', 'ADDRESS_OUT', 
              'LONG_LAT', 'TIGER_EDGE', 'STREET_SIDE', 'FIPS_STATE', 'FIPS_COUNTY', 
              'CENSUS_TRACT', 'CENSUS_BLOCK']

