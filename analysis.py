import pandas as pd, time
from datetime import datetime

all_data_location = 'all_data.csv'
cols = {'date': 'Date', 'dur': 'Time Spent (seconds)', 'people': 'Number of People', 'act': 'Activity', 'cat': 'Category', 'prod': 'Productivity'}
pd.options.display.max_rows = 100
STATS = ['Min', '25th', 'Median', '75th', 'Max', 'Mean', 'STD']
agg_func = {cols['dur']: 'sum', cols['cat']: 'first', cols['prod']: 'first'};
time_periods = ['Year', 'Month', 'Y-M', 'Y-M-D', 'DOW', 'Hour', 'Min']

def s2hms(seconds):
	try:
		seconds = int(seconds)
	except:
		seconds = 0
	return ':'.join([str(x) for x in [seconds//3600, (seconds%3600)//60, seconds%60]])

def parse_date(date):
	DOW = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
	spl = date.split('T')
	ymd = spl[0].split('-')
	ym = ymd[0] + '-' + ymd[1]
	dow = datetime(int(ymd[0]), int(ymd[1]), int(ymd[2])).weekday()
	return ([int(x) for x in ymd] + [ym, spl[0], DOW[dow]] + spl[1].split(':'))[:-1] #format is [Y, M, D, Y-M, Y-M-D, DOW, H, M]
	
def get_time_rank_for_year_act(act):
	ret = []
	for yr in years:
		if yr_act.index.isin([(yr, act)]).any():
			ret.append(yr_act.loc[yr, act][[cols['dur'], 'rank']])
		else:
			ret.append(pd.Series([0, -1], index=[cols['dur'], 'rank']))
	return ret

def first(x): return x.reset_index(drop=True)[0] if len(x) > 0 else None
def second(x): return x.reset_index(drop=True)[1] if len(x) > 1 else None
def third(x): return x.reset_index(drop=True)[2] if len(x) > 2 else None


# get data
df = pd.read_csv(all_data_location)


# make year, month, day, hour, min columns
df['Year'], df['Month'], df['Day'], df['Y-M'], df['Y-M-D'], df['DOW'], df['Hour'], df['Min'] = zip(*df[cols['date']].map(parse_date))
df = df[['Year', 'Month', 'Y-M', 'Y-M-D', 'DOW', 'Day', 'Hour', 'Min', cols['dur'], cols['act'], cols['cat'], cols['prod']]]
years = df['Year'].unique()

'''
Provide all analysis given a dataframe slice (time period)
'''
def analyze(df, all_data=False):
	start = time.time()

	TOTAL_SECONDS = df[cols['dur']].sum()
	TOTAL_HMS = s2hms(TOTAL_SECONDS)

	# group time by activity
	all_act = df.groupby(df[cols['act']]).agg(agg_func).sort_values(by=cols['dur'], ascending=False).reset_index()
	all_act.index += 1
	all_act['H:M:S'] = all_act.apply(lambda row: s2hms(row[cols['dur']]), axis=1)
	all_act = all_act[[cols['act'], cols['dur'], 'H:M:S', cols['cat'], cols['prod']]]

	# if all_data:
	# 	get trends of years for each activity (slow)
	# 	group on year and activity, add rank
	# 	yr_act = df.groupby(['Year', cols['act']]).agg(agg_func).sort_values(by=cols['dur'], ascending=False)
	# 	yr_act['rank'] = yr_act.groupby(level=0)[cols['dur']].rank(ascending=False)

	# 	# add year breakdowns
	# 	temp = list(zip(*all_act[cols['act']].map(get_time_rank_for_year_act)))
	# 	for i, year in enumerate(years):
	# 		all_act[str(year) + ' (hms)'] = [s2hms(x[cols['dur']]) for x in temp[i]]
	# 	for i, year in enumerate(years):
	# 		all_act[str(year) + ' (rank)'] = [int(x['rank']) if x['rank'] != -1 else '-' for x in temp[i]]

	'''
	Get the top activities for time period group, or category
	'''
	def get_top_times(group, sortby=cols['dur'], aggfunc=agg_func):
		# group by activity and time period
		df2 = df.groupby([group, cols['act']]).agg(aggfunc).sort_values(by=cols['dur'], ascending=False)
		df2['Cum Prod'] = df2[cols['dur']] * df2[cols['prod']]
		df2 = df2.reset_index()

		# get top activities, group cum prod
		df2 = df2.groupby(group).agg({cols['dur']: ['sum', first, second, third], cols['act']: [first, second, third], 'Cum Prod': 'sum'})
		df2['Cum Prod'] = ((df2['Cum Prod'] / df2[cols['dur']]) + 2)/4 # 0 - very unproductive, 0.5 - neutral, 1 - very productive
		
		# flatten and rename columns, get HMS from seconds, sort
		df2.columns = df2.columns.get_level_values(0)
		df2.columns = ['Time Spent (seconds)', 'Top HMS', '2nd HMS', '3rd HMS', 'Top Activity', '2nd Activity', '3rd Activity', 'Cum Prod']
		df2.sort_values(by=sortby, ascending=False, inplace=True)
		df2['H:M:S'] = df2.apply(lambda row: s2hms(row[cols['dur']]), axis=1)
		for col in ['Top HMS', '2nd HMS', '3rd HMS']:
			df2[col] = df2.apply(lambda row: s2hms(row[col]), axis=1)
		df2 = df2[['Time Spent (seconds)', 'H:M:S', 'Top Activity', 'Top HMS', '2nd Activity', '2nd HMS', '3rd Activity', '3rd HMS', 'Cum Prod']]
		
		# get stats
		dur, prod = df2[cols['dur']], df2['Cum Prod']
		dur_st = [s2hms(x) for x in [dur.min(), dur.quantile(.25), dur.median(), dur.quantile(.75), dur.max(), dur.mean(), dur.std()]]
		prod_st = [prod.min(), prod.quantile(.25), prod.median(), prod.quantile(.75), prod.max(), prod.mean(), prod.std()]
		l = range(len(STATS))
		stats_df = pd.DataFrame([{STATS[i]: dur_st[i] for i in l}, {STATS[i]: prod_st[i] for i in l}], index=['Duration', 'Productivity'])
		stats_df = stats_df[STATS]
		return stats_df, df2

	all_cat = get_top_times(cols['cat'], aggfunc={cols['dur']: 'sum', cols['prod']: 'first'})
	for group in time_periods:
		stats, group_df = get_top_times(group)
		print('Group: ' + group)
		print(stats)
		print()
		print(group_df.head(50))
		print('\n\n')

	print('TOP ACTIVITIES - ALL TIME')
	print(all_act.head(50))
	print()
	print('TOP CATEGORIES - ALL TIME')
	print(all_cat[1].head(50))
	print('Total time: ' + str(TOTAL_SECONDS) + ' seconds, or ' + TOTAL_HMS)
	print('Analysis finished in ' + str(time.time() - start) + ' seconds' + '\n' * 20)




######

# analyze on all data first
analyze(df, all_data=True)

def time_period():

	def parse_input(inp):
		try:
			begin, end = inp.split(' ')[0], inp.split(' ')[1]
			begin_date = datetime.strptime(begin, '%Y-%m-%d').date() # inclusive 
			end_date = datetime.strptime(begin, '%Y-%m-%d').date() # inclusive 
			if end_date < begin_date:
				return None
			begin_ymd = [int(x) for x in begin.split('-')]
			end_ymd = [int(x) for x in end.split('-')]
			return [begin_ymd, end_ymd]
		except:
			return None

	inp = input('Enter a specific time period (format: YYYY-MM-DD YYYY-MM-DD (start and end dates, inclusive)). Type EXIT to exit.\n> ')
	dates = parse_input(inp)
	if dates is None:
		print('Invalid entry.')
		time_period()
	begin, end = dates[0], dates[1]
	df = df.loc[df['Year'].isin(range(begin[0], end[0] + 1))]
	df = df.loc[df['Month'].isin(range(begin[1], end[1] + 1))]
	df = df.loc[df['Day'].isin(range(begin[2], end[2] + 1))]
	if df.empty:
		print('No data for this time')
		time_period()
	analyze(df)


def activity_analysis():

	activity = input('Enter an activity\n> ')
	for period in ['Y-M-D']:
		df2 = df.groupby([period, cols['act']]).agg(agg_func).sort_values(by=cols['dur'], ascending=False)
		df2['Period rank'] = df2.groupby(level=0)[cols['dur']].rank(ascending=False)
		print(df2.head(50))

		df2['Total time'] = df2.groupby(level=0).sum(axis=1)
		df2['% Period'] = 100 * df2[cols['dur']] / df2['Total time']
		#df2['Total time'] = df2.apply(lambda row: s2hms(row['Total time']), axis=1)
		df2 = df2.xs(activity, level=cols['act'], axis=0, drop_level=True)
		df2['Activity time'] = df2.apply(lambda row: s2hms(row[cols['dur']]), axis=1)
		df2 = df2[['Total time', 'Activity time', '% Period', 'Period rank']]
		print(df2.head(50))

def category_analysis():
	print('hello')

inp = input('Type 1 for time period analysis.\nType 2 for activity analysis.\nType 3 for category analysis\n> ')
while(inp != 'EXIT'):
	if inp == '1': time_period()
	elif inp == '2': activity_analysis()
	elif inp == '3': category_analysis()
	inp = input('Type 1 for time period analysis.\nType 2 for activity analysis.\nType 3 for category analysis\n> ')

















































