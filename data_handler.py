import pandas as pd
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from seaborn import histplot
import plotly.express as px
from plotly.offline import plot

class Handler():

    def __init__(self, path) -> None:
        self.path = path
        
    def prepare_data(self):
        self.df_raw = pd.read_csv(self.path)

        self.df = self.df_raw.copy()

        self.df[['Title','Subtitle']] = self.df['Title'].str.split(':', 1, expand=True).apply(lambda x: ':' if 'Title' in x else x)
        self.df2 = self.df[['Title', 'Date']]
        self.df2['Frequency'] = 1
        self.df2['Date'] = pd.to_datetime(self.df['Date']) + pd.offsets.MonthBegin(0)
        self.df1 = self.df['Title'].value_counts().rename_axis('Title').reset_index(name='Frequency')
        self.df = self.df.drop_duplicates(subset='Title')
        self.df = pd.merge(self.df, self.df1, on=['Title'])
        self.df = self.df.drop(['Subtitle'], axis=1)

        self.df_raw_list_all = pd.read_csv('NetflixList.csv')
        self.df_fullList = self.df_raw_list_all.copy()

        self.df_fullList['listed_in'] = self.df_fullList['listed_in'].str.replace('"', '')
        self.df_fullList['listed_in'] = self.df_fullList['listed_in'].str.replace('\'', '')
        self.df_fullList['listed_in'] = self.df_fullList['listed_in'].str.split(', ')
        self.df_fullList[['first_genre', 'second_genre', 'third_genre']] = pd.DataFrame(self.df_fullList['listed_in'].tolist()).astype('category')
        self.df = self.df.merge(self.df_fullList[['Title', 'first_genre', 'second_genre', 'third_genre']], how = 'inner', on='Title')

        self.df['Date'] = pd.to_datetime(self.df['Date']) + pd.offsets.MonthBegin(0)

    def run_plot(self):
        fig = px.line(self.df, x="Date", y="Frequency")
        plot(fig)
        fig = px.density_heatmap(self.df, x="first_genre", y="second_genre", z="Frequency" ,template="seaborn")
        plot(fig)
path = 'NetflixViewingHistory.csv'
c = Handler(path)
c.prepare_data()
c.run_plot()