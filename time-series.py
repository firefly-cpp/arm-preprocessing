from arm_preprocessing.timeseries import TimeSeries
from arm_preprocessing.dataset import Dataset

dataset = Dataset("datasets/measures2.txt")

dataframe = dataset.to_df_parse_dt()

series = TimeSeries(dataframe)

filters = series.filter_intervals('1Min')

print (filters)
