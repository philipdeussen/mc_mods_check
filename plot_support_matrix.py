# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import sys


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "mod_check_filesave.csv"

df = pd.read_csv(filename)
df.columns = df.columns.str.strip()

mod_names = df['mod_name'] + " (" +  df['server_client_use'] + ")"
mc_versions = df.drop(['mod_name','server_client_use'],axis=1).columns


# %%
df_mapped = df.replace({'release': 2, 'beta': 1, 'None':0}).fillna(0)
df_mapped.index = df_mapped['mod_name']
df_mapped = df_mapped.drop(['mod_name','server_client_use'],axis=1)



# %%
# Custom colormap
cmap = ListedColormap(['red', 'orange', 'green'])

# Create plot
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(
    df_mapped,
    ax=ax,
    cmap=cmap,
    linewidths=3,
    linecolor='white',
    cbar=False,
    square=False
)

# Axis formatting
ax.set_xticklabels(mc_versions, rotation=45, ha='right', fontsize=11)
ax.set_yticklabels(mod_names, fontsize=11, rotation=0)
ax.set_title("Mod Support Matrix", fontsize=15, pad=20)
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')


legend_elements = [
    Patch(facecolor='green', edgecolor='black', label='Release'),
    Patch(facecolor='orange', edgecolor='black', label='Beta'),
    Patch(facecolor='red', edgecolor='black', label='Nicht verfügbar'),
]
ax.legend(
    handles=legend_elements,
    title="Legend",
    loc='lower left',
    bbox_to_anchor=(1.01, 0),
    borderaxespad=0.,
    frameon=True
)


# Add datetime in bottom right
timestamp = datetime.datetime.now().strftime("Generated on %Y-%m-%d at %H:%M:%S")
fig.text(0.99, 0.01, timestamp, ha='right', va='bottom', fontsize=8, color='gray')

# Save with current day as filename
if len(sys.argv) >= 3:
    timestamp_filename = sys.argv[2]
else:
    timestamp_filename = datetime.datetime.now().strftime("mods_support_mat_%Y-%m-%d%H:%M:%S.png")

plt.tight_layout(pad=2.5)
plt.savefig(f"{timestamp_filename}", dpi=300)
#plt.show()
