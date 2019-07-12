import csv
import matplotlib.pyplot as plt 
import numpy as np 
import datetime

partial_path = 'data_by_month/'
years = ["2013", "2014", "2015", "2016", "2017", "2018"]
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

timeseries = []

for y in years:
	for m in months:
		timeseries.append(datetime.datetime(int(y), int(m), 1, 0, 0))
timeseries = np.array(timeseries)

cluster_by_category = {}

for y in years:
	for m in months:
		with open(partial_path + y + '/' + m + '.csv') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				if row[0] == 'App':
					continue
				category = row[2]
				time_spent = row[1]

				if category not in cluster_by_category:
					cluster_by_category[category] = {}
				if (y+m) not in cluster_by_category[category]:
					cluster_by_category[category][y+m] = 0
				cluster_by_category[category][y+m] += int(time_spent)

for category in cluster_by_category:
	time_spent = []
	for y in years:
		for m in months:
			time_spent.append(cluster_by_category[category].get(y+m, 0))
	p = plt.plot(timeseries, time_spent, label=category)

plt.xlabel('Year-Month')
plt.ylabel('Time Spent (seconds)')
plt.legend(bbox_to_anchor=(1, 1.125))
plt.show()

print("Number of categories: " + str(len(cluster_by_category.keys())))

