# %%
import pandas as pd
import json
import datetime
import sys
import os
import shutil

import helper_functions as hp

# %%
if len(sys.argv) > 1:
    mc_version = sys.argv[1]
else:
    sys.exit("No input argument for MC version could be found.")

# %%
data = hp.getModListFromFile()

# %% Create new directory for server and client mods separately
client_mod_dirname = "_mods_client"
server_mod_dirname = "_mods_server"
tmp_dir = "_tmp"

if not os.path.isdir(client_mod_dirname):
    os.mkdir(client_mod_dirname)
else:
    print("Client mod directory already existing.")

if not os.path.isdir(server_mod_dirname):
    os.mkdir(server_mod_dirname)
else:
    print("Server mod directory already existing.")

if not os.path.isdir(tmp_dir):
    os.mkdir(tmp_dir)
else:
    print("tmp mod directory already existing.")

# %%
for i in range(0,len(data)):
    mod_data = hp.getModrinthInfo(data['mod_name'][i])
    avail, iter = hp.getModAvailibility(mod_data, mc_version)
    if avail == 'None':
        sys.exit("Mod {mod_name} is not available for the given MC version.".format(mod_name=data['mod_name'][i]))
    else:
        file_obj = mod_data[iter]['files']
        if len(file_obj) > 1:
            file_iter = 0
            #sys.exit("Error: No unique file to download could be found for {mod_name}.".format(mod_name=data['mod_name'][i]))
        elif len(file_obj) == 0:
            sys.exit("No file to download could be found for mod {mod_name}.".format(mod_name=data['mod_name'][i]))
        else:
            file_iter = 0
        url = mod_data[iter]['files'][file_iter]['url']
        filename = mod_data[iter]['files'][file_iter]['filename']
        server_client_ref = data['server_client_use'][i]

        src_filepath = os.path.join(tmp_dir, filename)

        hp.downloadFile(url, src_filepath)
        # Copy to client-side mod directory if mod is used for client
        if 'c' in server_client_ref:
            shutil.copyfile(src_filepath, os.path.join(client_mod_dirname, filename))
        # Copy to server-side mod directory if mod is used for server
        if 's' in server_client_ref:
            shutil.copyfile(src_filepath, os.path.join(server_mod_dirname, filename))

# Zip both client and server mod directories
shutil.make_archive("client_mods_{mc_version}".format(mc_version=mc_version), 'zip', client_mod_dirname)
shutil.make_archive("server_mods._{mc_version}".format(mc_version=mc_version), 'zip', server_mod_dirname)

# Delete tmp directory
shutil.rmtree(tmp_dir)