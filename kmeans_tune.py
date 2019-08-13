from kmeans import kmeans
from metrics import sse, silhouette
from data_processing import get_data_points
import matplotlib.pyplot as plt

def run():
	max_k = int(input('Maximum number of clusters? '))
	metric = input('Desired metric? ')
	if metric=='sse':
		fn = sse
		title = 'Sum of Squared Errors'
	elif metric=='silhouette':
		fn = silhouette
		title = 'Silhouette Score'
	else:
		print('unrecognized metric')
		return
	points, apps, timeseries = get_data_points()

	val = {}
	length = len(points)

	num_clusters = list(range(1, max_k))

	for k in num_clusters:
		means, labels = kmeans(points, k)
		print('kmeans finished')
		val[k] = fn(points, means, labels)

	plt.plot(num_clusters, list(val.values()))
	plt.xlabel('Number of clusters (k)')
	plt.ylabel(title)
	plt.title("Hyperparameter Tuning")
	plt.show()

if __name__ == '__main__':
	run()