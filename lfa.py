import csv
import numpy as np 
import datetime
import matplotlib.pyplot as plt

partial_path = 'data_by_month/'
years = ["2013", "2014", "2015", "2016", "2017", "2018"]
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

timeseries = []

for y in years:
	for m in months:
		timeseries.append(datetime.datetime(int(y), int(m), 1, 0, 0))
timeseries = np.array(timeseries)

app_data_by_year_month = {}

rank = 4 #num clusters

top = 10 #num apps to look at in each cluster

for y in years:
	for m in months:
		with open(partial_path + y + '/' + m + '.csv') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				if row[0] == 'App':
					continue
				app = row[0]
				time_spent = row[1]

				if app not in app_data_by_year_month:
					app_data_by_year_month[app] = {}
				app_data_by_year_month[app][y+m] = np.log(int(time_spent)+1)

data = [] # u = app, v = year-month
u_map = {}
v_map = {}

i = 0

for app in app_data_by_year_month:
	u_map[i] = app
	i+=1

i = 0

for y in years:
	for m in months:
		v_map[i] = y+m
		i+= 1

for app in app_data_by_year_month:
	row_values = []
	for y in years:
		for m in months:
			row_values.append(app_data_by_year_month[app].get(y+m, 0))
	data.append(row_values)

data = np.matrix(data)

u, s, vh = np.linalg.svd(data, full_matrices=False)

approx_s = np.append(s[:rank], np.zeros(len(s)-rank))
approx = np.dot(np.dot(u, np.diag(approx_s)), vh)

for i in range(rank):
	print("Cluster " + str(i))
	print("----------------------------------------------------------------------------")
	related_apps = np.argsort(np.array(np.take(u, i, 1).tolist()[0]))
	related_year_months = np.argsort(vh[i].tolist()[0])
	print("Related Apps:")
	apps = []
	for j in range(top):
		apps.append(u_map[related_apps[j]])
	print(apps)
	print("Related year-months:")
	ym = []
	for j in range(top):
		ym.append(v_map[related_year_months[j]])
	print(ym)
	print('\n')

	mean = np.array([0 for i in range(72)]).astype(float)
	for j in range(top):
		mean += np.array(data[related_apps[j]].tolist()[0])

	mean /= top

	plt.plot(timeseries, mean, label="Cluster " + str(i))

plt.xlabel('Year-Month')
plt.ylabel('Mean Time spent (hours)')
plt.legend()
plt.show()




