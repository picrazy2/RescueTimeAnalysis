import csv
import datetime
import numpy as np

def get_data_points():
	partial_path = 'data_by_month/'
	years = ["2013", "2014", "2015", "2016", "2017", "2018"]
	months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

	timeseries = []

	for y in years:
		for m in months:
			timeseries.append(datetime.datetime(int(y), int(m), 1, 0, 0))
	timeseries = np.array(timeseries)

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
	return np.array(points), apps, timeseries