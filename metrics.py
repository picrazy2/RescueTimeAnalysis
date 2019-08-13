import numpy as np
from scipy.spatial import distance_matrix

def sse(points, means, labels):
	s = 0
	for i in range(len(points)):
		s += np.linalg.norm(points[i] - means[labels[i]])**2
	return s

def silhouette(points, means, labels):
	length = len(points)
	storage = [[0, {}]] * length
	clusters = {}
	for i in range(length):
		if labels[i] not in clusters:
			clusters[labels[i]] = []
		clusters[labels[i]].append(points[i])
	X = np.matrix(points)
	d_matrix = distance_matrix(X, X)
	for i in range(length):
		for j in range(i+1, length):
			d = d_matrix[i][j]
			if labels[i] == labels[j]:
				storage[i][0] += d
				storage[j][0] += d
			else:
				storage[i][1][labels[j]] = storage[i][1].get(labels[j], 0) + d
				storage[j][1][labels[i]] = storage[j][1].get(labels[i], 0) + d
	print('distance calculations finished')
	s_scores = []
	fn = lambda t: (1.0/len(clusters[t[0]]))*t[1]
	k = len(clusters.keys())
	for i in range(length):
		if len(clusters[labels[i]]) == 1:
			s_scores.append(0)
		elif k > 1:
			a = (1.0/len(clusters[labels[i]])) * storage[i][0]
			b = min(list(map(fn, list(storage[i][1].items()))))
			s_scores.append((b-a)/max(b, a))
		else:
			s_scores.append(-1)
	return np.mean(s_scores)