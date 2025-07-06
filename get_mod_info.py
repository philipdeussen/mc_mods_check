# %%
import requests
import pandas as pd
import json
import datetime
import sys

# Minecraft versions against which the availability of all mods
# defined above is to be checked.
mc_versions = ['1.21.4', '1.21.5', '1.21.6', '1.21.7']


# Define helper functions

def getModrinthInfo(mod_name):
    api_url = "https://api.modrinth.com/v2/project/{mod_name}/version"
    response = requests.get(api_url.format(mod_name=mod_name))
    response.raise_for_status()
    data = response.json()
    return data


# %%
# Read mods from csv and add column headers for MC versions
data = pd.read_csv("mods.csv")
for v in mc_versions:
    data[v.strip()] = ''
data.columns = data.columns.str.strip()

# %% 
# Iterate over all mods and check availability for specified MC versions
for i in range(0,len(data)):
    mod_data = getModrinthInfo(data['mod_name'][i])
    for v in mc_versions:
        data.loc[i, v] = 'None'
        for j in range(0, len(mod_data)):
            elem = mod_data[j]
            # Check only game version if loader is fabric
            if 'fabric' in elem['loaders']:
                if v in elem['game_versions']:
                    data.loc[i, v] = elem['version_type']
                    break;




# %%
# Save dataframe to file with timestamp or external input
if len(sys.argv) > 1:
    timestamp_filename = sys.argv[1]
else:
    timestamp_filename = datetime.datetime.now().strftime("mods_check_%Y-%m-%d%H:%M:%S")
data.to_csv(timestamp_filename, encoding='utf-8', index=False, header=True)