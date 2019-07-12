import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime

partial_path = 'data_by_month/'
years = ["2013", "2014", "2015", "2016", "2017", "2018"]
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

timeseries = []

for y in years:
	for m in months:
		timeseries.append(datetime.datetime(int(y), int(m), 1, 0, 0))
timeseries = np.array(timeseries)

NUM_CLUSTERS = 7

def kmeans(p):
	length = len(points)
	mean_indices = np.random.randint(length, size=NUM_CLUSTERS)
	means = []
	for i in mean_indices:
		means.append(p[i])
	clusters = []

	for i in range(length):
		dists = []
		for mu in means:
			dists.append(np.linalg.norm(np.matrix(p[i]) - np.matrix(mu)))
		clusters.append(np.argmin(dists))

	newlabels = length

	while newlabels > 0:
		#step 1: fix y, update u
		means.clear()
		points_in_cluster = {}
		for i in range(length):
			if clusters[i] not in points_in_cluster:
				points_in_cluster[clusters[i]] = []
			points_in_cluster[clusters[i]].append(p[i])
		for c in points_in_cluster:
			means.append(np.array(np.matrix(points_in_cluster[c]).mean(0).tolist()[0]))

		#step 2; fix u, update y
		newlabels = 0
		for i in range(length):
			dists = []
			for mu in means:
				dists.append((np.linalg.norm(p[i] - mu)))
			label = np.argmin(dists)
			if clusters[i] != label:
				newlabels += 1
			clusters[i] = label

	return means, clusters

# main
app_data_by_year_month = {}

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
				app_data_by_year_month[app][y+m] = int(time_spent)

points = []
apps = []
for app in app_data_by_year_month:
	point = []
	for y in years:
		for m in months:
			point.append(app_data_by_year_month[app].get(y+m, 0))
	points.append(point)
	apps.append(app)

means, labels = kmeans(points)

points_in_cluster = {}
for i in range(len(labels)):
	if labels[i] not in points_in_cluster:
		points_in_cluster[labels[i]] = {}
	points_in_cluster[labels[i]][apps[i]] = True

f = open('clusters.txt', 'w')

for i in points_in_cluster:
	print('Cluster ' + str(i+1) + ': ')
	f.write("Cluster " + str(i+1) + '\n')
	print("----------------------------------------------------------------------------")
	apps = list(points_in_cluster[i].keys())
	for app in apps:
		f.write(str(app) + '\n')
	print("Related Apps:")
	print(apps)
	print("Cluster Average (seconds):")
	print(means[i].astype(int))
	print('\n')

	plt.plot(timeseries, means[i], label="Cluster " + str(i+1))

f.close()

f = open('kmeans_results.txt', 'w')
for i in points_in_cluster:
	f.write('Cluster ' + str(i+1) + '\n')
	apps = list(points_in_cluster[i].keys())
	for app in apps:
		f.write(str(app) + '\n')
f.close()

plt.xlabel('Year-Month')
plt.ylabel('Mean Time spent (seconds)')
plt.legend(bbox_to_anchor=(1, 1.125))
plt.show()






