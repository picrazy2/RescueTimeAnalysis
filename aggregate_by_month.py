import csv
import os

by_year = {}

category = {}
productivity = {}

with open('all_data.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		if row[1] == 'Date':
			continue
		if row[4] == 'newtab':
			continue
		s = row[1].split('-')
		year = s[0]
		month = s[1]
		
		year_hash = by_year.get(year, {})
		by_month = year_hash.get(month, {})
		by_month[row[4]] = by_month.get(row[4], 0) + int(row[2])
		category[row[4]] = row[5]
		productivity[row[4]] = row[6]
		year_hash[month] = by_month
		by_year[year] = year_hash

for y in by_year:
	year = by_year[y]
	try:
		os.makedirs('data_by_month/' + y, exist_ok=True)
	except FileExistsError:
		pass
	for m in year:
		filename = 'data_by_month/' + y + '/' + m + '.csv'
		with open(filename, 'w') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(['App', 'Time Spent (Seconds)', 'Category', 'Productivity'])
			month = year[m]
			for app in month:
				writer.writerow([app, month[app], category[app], productivity[app]])







