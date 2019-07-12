import csv
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation


CATEGORIES = ['Video', 'General Utilities', 'General Social Networking', 'Video Editing',
'General Reference & Learning', 'Writing', 'General Software Development']

x_labels = ['Video', 'Utilities', 'Social Networking', 'Video Editing', 'Learning', 'Writing', 'Software Dev']

years = ["2013", "2014", "2015", "2016", "2017", "2018"]
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

ym = {}
ym['title'] = {}
i = 0
for y in years:
	for m in months:
		path = 'data_by_month/' + y + '/' + m + '.csv'
		time_spent_per_category = {}
		with open(path) as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				if row[0] == 'App':
					continue
				category = row[2]
				time_spent = row[1]
				if category not in time_spent_per_category:
					time_spent_per_category[category] = 0
				time_spent_per_category[category] += int(time_spent)/3600.0
		y_values = []
		for c in CATEGORIES:
			y_values.append(time_spent_per_category.get(c, 0))
		ym[i] = y_values
		ym['title'][i] = y + '-' + m
		i += 1

def animate(i):
	y = ym[i]
	plt.cla()
	plt.xlabel('Category')
	plt.ylabel("Time spent per month (hours)")
	plt.title(ym['title'][i])
	plt.ylim(0, 100)
	return plt.bar(x_labels, y)


fig, ax = plt.subplots()

plt.xlabel('Category')
plt.ylabel("Time spent per month (hours)")

ani = FuncAnimation(fig, animate, frames=72, interval=100, blit=False, repeat=False)
# animate(1)
plt.show()