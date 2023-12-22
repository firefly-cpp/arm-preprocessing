from arm_preprocessing.timeseries import TimeSeries
from arm_preprocessing.dataset import Dataset

dataset = Dataset('datasets/measures2', format='txt',
                  datetime_columns=['date', 'time'])
dataset.load()

series = TimeSeries(dataset.data)

filters = series.filter_intervals('1Min')

print(filters)
