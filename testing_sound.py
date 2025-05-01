#%%
import pandas as pd

file = "/mnt/c/Users/HMARTINEZ/Desktop/sound_calibration_tocheck_weird_stuff.csv"
df = pd.read_csv(file, sep=";")

df.head()
#%%
import seaborn as sns

sns.scatterplot(data=df, x="gain", y="dB_obtained", hue="frequency")
# %%
