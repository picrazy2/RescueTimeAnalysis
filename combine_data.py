import pandas as pd, os

data_location = 'data/'
all_data_location = 'all_data.csv'
all_data = None

file_list = sorted(os.listdir(data_location))
print(str(len(file_list)) + ' total files')

for i, filename in enumerate(file_list):
    if filename.endswith(".csv"):
        all_data = pd.concat([all_data, pd.read_csv(data_location + filename)]);
    if (i+1) % 100 == 0:
    	print(str(i+1) + ' files concatenated')
print('Files concatenated')

all_data.to_csv(all_data_location)
