import requests
import urllib.request
import pandas as pd

def getModrinthInfo(mod_name):
    api_url = "https://api.modrinth.com/v2/project/{mod_name}/version"
    response = requests.get(api_url.format(mod_name=mod_name))
    response.raise_for_status()
    data = response.json()
    return data


def getModAvailibility(mod_data, version_number):
    avail = 'None'
    for j in range(0, len(mod_data)):
            elem = mod_data[j]
            # Check only game version if loader is fabric
            if 'fabric' in elem['loaders']:
                if version_number in elem['game_versions']:
                    avail = elem['version_type']
                    break;
    iter = j
    return avail, iter


def getModListFromFile():
    data = pd.read_csv("mods.csv")
    data.columns = data.columns.str.strip()
    return data

def downloadFile(url, filename):
    urllib.request.urlretrieve(url, filename)