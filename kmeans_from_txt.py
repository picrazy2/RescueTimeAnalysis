import matplotlib.pyplot as plt 
import datetime
import numpy as np
import csv

years = ["2013", "2014", "2015", "2016", "2017", "2018"]
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

timeseries = []
for y in years:
	for m in months:
		timeseries.append(datetime.datetime(int(y), int(m), 1, 0, 0))
timeseries = np.array(timeseries)

f = open('saved_results/1.txt', 'r')

lines = list(f)

cluster_apps = {}
clusters = []
app_cluster_map = {}

cluster = None
for line in lines:
	if 'Cluster' in line:
		cluster = int(line[-2])
		clusters.append(cluster)
	else:
		if cluster not in cluster_apps:
			cluster_apps[cluster] = []
		cluster_apps[cluster].append(line[:-1])
		app_cluster_map[line[:-1]] = cluster

cluster_data = {}
partial_path = 'data_by_month/'
for y in years:
	for m in months:
		filename = partial_path + y + '/' + m + '.csv'
		with open(filename, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				if row[0] == 'App':
					continue
				app = row[0]
				time_spent = row[1]
				if app_cluster_map[app] not in cluster_data:
					cluster_data[app_cluster_map[app]] = {}
				if (y+m) not in cluster_data[app_cluster_map[app]]:
					cluster_data[app_cluster_map[app]][y+m] = 0
				cluster_data[app_cluster_map[app]][y+m] += int(time_spent)

for c in clusters:
	size = len(cluster_apps[c])
	mean = []
	for y in years:
		for m in months:
			mean.append(cluster_data[c].get((y+m), 0)/ size)
	plt.plot(timeseries, mean, label='Cluster ' + str(c))
	print('Cluster ' + str(c) + ': ')
	print("----------------------------------------------------------------------------")
	apps = cluster_apps[c]
	print("Related Apps:")
	print(apps)
	print("Cluster Average (seconds):")
	print(mean)
	print('\n')


plt.xlabel('Year-Month')
plt.ylabel('Mean Time spent (seconds)')
plt.legend(bbox_to_anchor=(1, 1.125))
plt.show()