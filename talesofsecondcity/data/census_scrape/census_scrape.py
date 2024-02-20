from data.census_scrape import variable_defs
from census import Census
from us import states
import pandas as pd
import requests


def extract_2012_ACS5_data(key = "7afa3a5a9a46932f7041a1b98355987a68b69cbc"):
    """
    Use the Census python package to interact with Census API and collect race,
    income, age, home ownership and educational attainment data published in 
    2012.

    Inputs: API Key 

    Outputs: ??
    """

    c = Census(key)
    variables_2012 = ("NAME",) + tuple(variable_defs.variables_2012.keys())

    data_2012 = c.acs5dp.state_county_tract(variables_2012, states.IL.fips, '031', 
                                                   Census.ALL, year = 2012)
    data_2012 = pd.DataFrame(data_2012)
    data_2012 = data_2012.rename(columns = variable_defs.variables_2012)



def extract_2017_ACS5_data(key = "7afa3a5a9a46932f7041a1b98355987a68b69cbc"):
    """
    Use the Census python package to interact with Census API and collect race,
    income, age, home ownership and educational attainment data published in 
    2017.

    Inputs: API Key 

    Outputs: ??
    """

    c = Census(key)
    variables_2017 = ("NAME",) + tuple(variable_defs.variables_2017.keys())

    data_2017 = c.acs5dp.state_county_tract(variables_2017, states.IL.fips, '031', 
                                            Census.ALL, year = 2017)
    
    data_2017 = pd.DataFrame(data_2017)
    data_2017 = data_2017.rename(columns = variable_defs.variables_2017)


def extract_2022_acs5_data(key = "7afa3a5a9a46932f7041a1b98355987a68b69cbc"): 
    """
    Create Census API Query for 2022 -- workaround function to accomdate for 
    the fact that the 2022 census data is not yet in the Census python package.

    Input: API Key 

    Output: ???
    """
    # code based loosely on Jennifer Yeaton's code (Snow Laughing Matter, 2023)

    base_url = "https://api.census.gov/data/2021/acs/acs5/profile?get="
    variables_2022 = "NAME," + ",".join(variable_defs.variables_2022.keys())

    # feeling unsure about the tract portion of this and need to come back to look at it
    geo_string = "&for=tract:*&in=county:031&in=state:17"
    key_string = "&key=" + key

    full_2022_query = f"{base_url}{variables_2022}{geo_string}{key_string}"

    # make API request and convert to pandas df
    data_2022 = requests.get(full_2022_query)
    
    col_names = ["Name"] + list(variable_defs.variables_2022.values()) + \
        ["State code", "County code", "Tract Code"]
    data_2022 = pd.DataFrame(data = data_2022.json()[1:], 
                             columns = col_names)
