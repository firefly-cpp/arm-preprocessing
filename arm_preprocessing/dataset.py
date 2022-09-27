import pandas as pd

class Dataset:
    def __init__(self, filename):
        self.filename = filename

    def to_df(self):
        return pd.read_csv(self.filename)

    def to_df_parse_dt(self):
        return pd.read_csv(self.filename, parse_dates=[['date', 'time']])
