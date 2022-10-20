import pandas as pd
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from seaborn import histplot

df_raw = pd.read_csv('NetflixViewingHistory.csv')

df = df_raw.copy()

df[['Title','Subtitle']] = df['Title'].str.split(':', 1, expand=True).apply(lambda x: ':' if 'Title' in x else x)
df1 = df['Title'].value_counts().rename_axis('Title').reset_index(name='Frequency')
df = df.drop_duplicates(subset='Title')
df = pd.merge(df, df1, on=['Title'])
df = df.drop(['Subtitle'], axis=1)

df_raw_list_all = pd.read_csv('NetflixList.csv')
df_fullList = df_raw_list_all.copy()

df = df.merge(df_fullList[['Title', 'listed_in']], how = 'inner', on='Title')
df_fullList['listed_in'] = df_fullList['listed_in'].str.replace('"', '')
df_fullList['listed_in'] = df_fullList['listed_in'].str.split(', ')
df_fullList[['first_genre', 'second_genre', 'third_genre']] = pd.DataFrame(df_fullList['listed_in'].tolist())

df['listed_in'] = df['listed_in'].str.replace('"', '')
df['listed_in'] = df['listed_in'].str.replace('\'', '')
df['listed_in'] = df['listed_in'].str.split(', ')
df[['first_genre', 'second_genre', 'third_genre']] = pd.DataFrame(df['listed_in'].tolist())
df = df.drop(['listed_in'], axis=1)

df_temp = df.groupby(['first_genre']).Title.value_counts()

sns.histplot(data = df_temp, y="first_genre")
plt.show()


