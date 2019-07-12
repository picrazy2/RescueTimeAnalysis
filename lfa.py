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

app_data_in_log_seconds = {}
app_data_in_seconds = {}

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

				if app not in app_data_in_log_seconds:
					app_data_in_log_seconds[app] = {}
					app_data_in_seconds[app] = {}
				app_data_in_log_seconds[app][y+m] = np.log(int(time_spent)+1)
				app_data_in_seconds[app][y+m] = int(time_spent)


data = [] # u = app, v = year-month
raw_data = []
u_map = {}
v_map = {}

i = 0

for app in app_data_in_log_seconds:
	u_map[i] = app
	i+=1

i = 0

for y in years:
	for m in months:
		v_map[i] = y+m
		i+= 1

for app in app_data_in_log_seconds:
	row_values = []
	raw_row_values = []
	for y in years:
		for m in months:
			row_values.append(app_data_in_log_seconds[app].get(y+m, 0))
			raw_row_values.append(app_data_in_seconds[app].get(y+m, 0))
	data.append(row_values)
	raw_data.append(raw_row_values)

data = np.matrix(data)

u, s, vh = np.linalg.svd(data, full_matrices=False)

saved_file = open('clusters.txt', 'w')

for i in range(rank):
	u_i = np.array(np.take(u, i, 1).tolist()[0])
	v_i = vh[i].tolist()[0]

	print("Cluster " + str(i+1))
	saved_file.write('Cluster ' + str(i+1) + '\n')
	print("----------------------------------------------------------------------------")
	related_apps = np.argsort(u_i)
	related_year_months = np.argsort(v_i)
	print("Related Apps:")
	apps = []
	membership = []
	for j in range(1, top+1):
		apps.append(u_map[related_apps[-j]])
		membership.append(u_i[related_apps[-j]])

		saved_file.write(str(u_map[related_apps[-j]]) + '\n')
	print(apps)
	print(membership)
	print("Related year-months:")
	ym = []
	membership = []
	for j in range(1, top+1):
		ym.append(v_map[related_year_months[-j]])
		membership.append(v_i[related_year_months[-j]])
	print(ym)
	print(membership)
	print('\n')

	mean = np.array([0 for i in range(72)]).astype(float)
	for j in range(1, top+1):
		mean += np.array(data[related_apps[-j]].tolist()[0])
		# mean += np.array(raw_data[related_apps[-j]])

	mean /= top

	plt.plot(timeseries, mean, label="Cluster " + str(i+1))

saved_file.close()

plt.xlabel('Year-Month')
plt.ylabel('Mean Time spent (log seconds)')
# plt.ylabel('Mean Time spent (seconds)')
plt.legend(bbox_to_anchor=(1, 1.125))
plt.show()




