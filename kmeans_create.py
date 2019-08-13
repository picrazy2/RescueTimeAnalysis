import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime
from kmeans import kmeans
from data_processing import get_data_points

def run():
	NUM_CLUSTERS = int(input('Number of clusters? '))
	points, apps, timeseries = get_data_points()

	means, labels = kmeans(points, NUM_CLUSTERS)

	colors = plt.cm.jet(np.linspace(0, 1, NUM_CLUSTERS))
	handles = []

	f1 = plt.figure(1)

	points_in_cluster = {}
	for i in range(len(labels)):
		if labels[i] not in points_in_cluster:
			points_in_cluster[labels[i]] = []
		points_in_cluster[labels[i]].append(apps[i])
		plt.plot(timeseries, points[i], color=colors[labels[i]])
	plt.title("Clusters")
	plt.xlabel('Year-Month')
	plt.ylabel('Mean Time spent (seconds)')
	plt.ylim(0, 200000)

	f = open('clusters.txt', 'w')
	f2 = plt.figure(2)
	for i in sorted(points_in_cluster.keys()):
		print('Cluster ' + str(i+1) + ': ')
		f.write("Cluster " + str(i+1) + '\n')
		print("----------------------------------------------------------------------------")
		apps = points_in_cluster[i]
		for app in apps:
			f.write(str(app) + '\n')
		print("Related Apps:")
		print(apps)
		print("Cluster Average (seconds):")
		print(means[i].astype(int))
		print('\n')

		handles.append(mpatches.Patch(color=colors[i], label="Cluster " + str(i+1)))

		plt.plot(timeseries, means[i], color=colors[i])
	plt.title("Cluster Centroids")
	plt.xlabel('Year-Month')
	plt.ylabel('Mean Time spent (seconds)')
	plt.ylim(0, 200000)
	plt.legend(handles=handles)
	f.close()

	f = open('index.txt', 'r')
	index = int(list(f)[0]) #next index to save to
	f.close()

	f = open('saved_results/' + str(index) + '.txt', 'w')
	for i in points_in_cluster:
		f.write('Cluster ' + str(i+1) + '\n')
		apps = points_in_cluster[i]
		for app in apps:
			f.write(str(app) + '\n')
	f.close()

	f = open('index.txt', 'w')
	f.write(str(index+1))
	f.close()

	plt.show()

if __name__ == '__main__':
	run()






