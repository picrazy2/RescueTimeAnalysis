import numpy as np
from scipy.spatial import distance_matrix

def kmeans(p, k):
	length = len(p)
	mean_indices = np.random.randint(length, size=k)
	means = []
	for i in mean_indices:
		means.append(p[i])
	clusters = []
	means = np.array(means)

	dm = distance_matrix(p, means)
	for i in range(length):
		clusters.append(np.argmin(dm[i:i+1]))

	newlabels = length

	while newlabels > 0:
		#step 1: fix y, update u
		means = np.empty((k, len(p[0])))
		points_in_cluster = {}
		for i in range(length):
			if clusters[i] not in points_in_cluster:
				points_in_cluster[clusters[i]] = []
			points_in_cluster[clusters[i]].append(p[i])
		for c in points_in_cluster:
			means[c] = np.array(points_in_cluster[c]).mean(0)

		#step 2; fix u, update y
		newlabels = 0
		dm = distance_matrix(p, means)
		for i in range(length):
			label = np.argmin(dm[i:i+1])
			if clusters[i] != label:
				newlabels += 1
			clusters[i] = label

	return means, clusters
 	
