import pandas as pd

class TimeSeries:
    def __init__(self, df):
        self.df = df

    def filter_intervals(self, freq):
        return {n: g for n, g in self.df.groupby(pd.Grouper(key='date_time', freq=freq))}
