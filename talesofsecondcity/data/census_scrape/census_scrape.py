
from census import Census
from us import states

c = Census(key = "7afa3a5a9a46932f7041a1b98355987a68b69cbc")
c.acs5dp.state_county_tract(("NAME","DP03_0062E", "DP04_0046PE"), states.IL.fips, '031', Census.ALL, year = 2017)



# import requests
# from pprint import pprint

# url = "https://api.census.gov/data/2022/acs/acs5/profile/variables.json"
# # let library handle URL parameters
# params = {"search": "distribution_pattern:nationwide",
#           "limit": 2}

# response = requests.get(url, params)
# # response objects have built in .json() method for decoding
# pprint(response.json())