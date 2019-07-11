import csv
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

partial_path = 'data_by_month/'
years = ["2013", "2014", "2015", "2016", "2017", "2018", "2019"]
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

NUM_CLUSTERS = 5

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

# for year in years:
with open(partial_path + '2018/05.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')

	points = [] #(productivity, time spent)
	apps = []
	for row in reader:
		if row[0] == 'App':
			continue
		points.append(np.array([int(row[3]), float(row[1]/3600)]))
		apps.append(row[0])
	means, labels = kmeans(points)

	points_in_cluster = {}
	for i in range(len(labels)):
		if labels[i] not in points_in_cluster:
			points_in_cluster[labels[i]] = {}
		points_in_cluster[labels[i]][apps[i]] = True

	for i in points_in_cluster:
		print('Cluster ' + str(i) + ': ')
		print('Average time spent in hours: ' + str(means[i][1]))
		print('Average productivity: ' + str(means[i][0]))
		print(list(points_in_cluster[i].keys()))


	# fig = plt.figure()
	# ax = fig.add_subplot(111, projection='3d')

	# ax.scatter(np.take(points, 0, 1), np.take(points, 1, 1), np.take(points, 2, 1), c=labels)

	# ax.set_xlabel('Month')
	# ax.set_ylabel('Productivity')
	# ax.set_zlabel("Time Spent (Hours)")
	# plt.show()




