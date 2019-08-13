import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import datetime
import numpy as np
import csv
from data_processing import get_data_points

def run():
	filename = input('Select saved results index: ')
	points, apps, timeseries = get_data_points()

	f = open('saved_results/' + filename + '.txt', 'r')
	lines = list(f)

	cluster_apps = {}
	app_cluster_map = {}


	cluster = None
	for line in lines:
		if 'Cluster' in line:
			cluster = int(line.split(" ")[-1])
		else:
			if cluster not in cluster_apps:
				cluster_apps[cluster] = []
			cluster_apps[cluster].append(line[:-1])
			app_cluster_map[line[:-1]] = cluster

	clusters = sorted(cluster_apps.keys())

	f1 = plt.figure(1)
	colors = plt.cm.jet(np.linspace(0, 1, clusters[-1]))
	means = [0] * clusters[-1]
	for i in range(len(points)):
		means[app_cluster_map[apps[i]]-1] += points[i]
		plt.plot(timeseries, points[i], color=colors[app_cluster_map[apps[i]]-1])
	plt.title('Clusters')
	plt.xlabel('Year-Month')
	plt.ylabel('Mean Time spent (seconds)')
	plt.ylim(0, 200000)

	for i in range(len(means)):
		means[i] = means[i]/len(cluster_apps[i+1])

	f2 = plt.figure(2)
	handles = []
	for c in clusters:
		plt.plot(timeseries, means[c-1], label='Cluster ' + str(c), color=colors[c-1])
		print('Cluster ' + str(c) + ': ')
		print("----------------------------------------------------------------------------")
		apps = cluster_apps[c]
		print("Related Apps:")
		print(apps)
		print("Cluster Average (seconds):")
		print(means[c-1])
		print('\n')
		handles.append(mpatches.Patch(color=colors[c-1], label="Cluster " + str(c)))

	plt.title('Cluster Centroids')
	plt.xlabel('Year-Month')
	plt.ylabel('Mean Time spent (seconds)')
	plt.ylim(0, 200000)
	plt.legend(handles=handles)
	plt.show()

if __name__ == '__main__':
	run()