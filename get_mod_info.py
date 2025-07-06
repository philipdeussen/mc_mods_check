# %%
import requests
import pandas as pd
import json
import datetime
import sys

import helper_functions as hp

# Minecraft versions against which the availability of all mods
# defined above is to be checked.
mc_versions = ['1.21.4', '1.21.5', '1.21.6', '1.21.7']

# %%
# Read mods from csv and add column headers for MC versions
data = hp.getModListFromFile()
for v in mc_versions:
    data[v.strip()] = ''
data.columns = data.columns.str.strip()

# %% 
# Iterate over all mods and check availability for specified MC versions
for i in range(0,len(data)):
    mod_data = hp.getModrinthInfo(data['mod_name'][i])
    for v in mc_versions:
        data.loc[i, v] = hp.getModAvailibility(mod_data, v)
        


# %%
# Save dataframe to file with timestamp or external input
if len(sys.argv) > 1:
    timestamp_filename = sys.argv[1]
else:
    timestamp_filename = datetime.datetime.now().strftime("mods_check_%Y-%m-%d%H:%M:%S")
data.to_csv(timestamp_filename, encoding='utf-8', index=False, header=True)