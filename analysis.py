import pandas as pd, time, os
import datetime
import matplotlib.pyplot as plt

all_data_location = 'all_data.csv'
cols = {'date': 'Date', 'dur': 'Time Spent (seconds)', 'people': 'Number of People', 'act': 'Activity', 'cat': 'Category', 'prod': 'Productivity'}
pd.options.display.max_rows = 100
pd.set_option('precision', 2)

STATS = ['Min', '25th', 'Median', '75th', 'Max', 'Mean', 'STD']
agg_func = {cols['dur']: 'sum', cols['cat']: 'first', cols['prod']: 'first'};
time_periods = ['Year', 'Month', 'Y-M', 'Y-W', 'Y-M-D', 'DOW', 'Hour', 'Min']

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
	week = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2])).isocalendar()[1]
	yw = ymd[0] + 'w' + str(week).zfill(2)
	dow = datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2])).weekday()
	return ([int(x) for x in ymd] + [ym, yw, spl[0], DOW[dow]] + spl[1].split(':'))[:-1] #format is [Y, M, D, Y-M, Y-W, Y-M-D, DOW, H, M]
	
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
times = ['Year', 'Month', 'Y-M', 'Y-W', 'Y-M-D', 'DOW', 'Day', 'Hour', 'Min']
df['Year'], df['Month'], df['Day'], df['Y-M'], df['Y-W'], df['Y-M-D'], df['DOW'], df['Hour'], df['Min'] = zip(*df[cols['date']].map(parse_date))
df = df[times + [cols['dur'], cols['act'], cols['cat'], cols['prod']]]
years = df['Year'].unique()

# make folders
if not os.path.exists('queries/'): os.makedirs('queries/')
folder_name = 'queries/runtime_' + str(time.time()) + '/'
time_period_dir = folder_name + 'time_period/'
activity_dir = folder_name + 'activity/'
category_dir = folder_name + 'category/'
if not os.path.exists(folder_name): os.makedirs(folder_name)
if not os.path.exists(time_period_dir): os.makedirs(time_period_dir)
if not os.path.exists(activity_dir): os.makedirs(activity_dir)
if not os.path.exists(category_dir): os.makedirs(category_dir)

'''
Provide all analysis given a dataframe slice (time period)
'''
def analyze(df, s, e, num_days, all_data=False):
	start = time.time()
	spec_dir = time_period_dir + s + '_' + e + '/' if not all_data else time_period_dir + 'ALL_DATA/'
	if not os.path.exists(spec_dir): os.makedirs(spec_dir)

	TOTAL_SECONDS = df[cols['dur']].sum()
	TOTAL_HMS = s2hms(TOTAL_SECONDS)

	# group time by activity
	all_act = df.groupby(df[cols['act']]).agg(agg_func).sort_values(by=cols['dur'], ascending=False).reset_index()
	all_act.index += 1
	all_act['H:M:S'] = all_act.apply(lambda row: s2hms(row[cols['dur']]), axis=1)
	all_act = all_act[[cols['act'], cols['dur'], 'H:M:S', cols['cat'], cols['prod']]]

	# plot top 20
	TOP_NUM = 20
	if num_days > 366: group = 'Y-M' 
	elif num_days > 60: group = 'Y-W'
	else: group = 'Y-M-D'
	#window = 3 if num_days > 366 else 7
	trend = df.groupby([group, cols['act']]).agg({cols['dur']: 'sum'})
	trend[cols['dur']] = trend[cols['dur']] / 3600
	trend = trend.unstack(level=-1)
	trend.columns = trend.columns.droplevel()
	top_x = df.groupby(cols['act']).agg(agg_func).sort_values(by=cols['dur'], ascending=False).head(TOP_NUM).index.tolist()
	trend['Total'] = trend.sum(axis=1)
	trend['Other'] = trend['Total'] - trend[top_x].sum(axis=1)
	trend = trend[(top_x + ['Other'])[::-1]]
	# roll here
	#trend = trend.rolling(window=window).mean()
	#print(trend)
	ax = trend.plot.area(title='Top ' + str(TOP_NUM) + ' Activities For Date Range ' + str(s) + ' ' + str(e), figsize=(20, 10))
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(reversed(handles), reversed(labels))
	ax.set_ylabel("# Hours")
	plt.savefig(spec_dir + 'activity_trend.png')
	#plt.show(block=False)

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
		stats.to_csv(spec_dir + group + '_stats.csv', encoding='utf-8')
		group_df.to_csv(spec_dir + group + '.csv', encoding='utf-8')
		print('Group: ' + group)
		print(stats)
		print()
		print(group_df.head(50))
		print('\n\n')

	all_act.to_csv(spec_dir + 'TOP_ACTIVITIES.csv', encoding='utf-8')
	all_cat[1].to_csv(spec_dir + 'TOP_CATEGORIES.csv', encoding='utf-8')

	print('TOP ACTIVITIES')
	print(all_act.head(50))
	print()
	print('TOP CATEGORIES')
	print(all_cat[1].head(50))
	print('Total time: ' + str(TOTAL_SECONDS) + ' seconds, or ' + TOTAL_HMS)
	print('Analysis finished in ' + str(time.time() - start) + ' seconds' + '\n' * 20)




###### ANALYSIS STARTS HERE #######

# analyze on all data first
analyze(df, '2013-01-01', '2019-07-12', 999999, all_data=True)

def time_period():

	def parse_input(inp):
		try:
			begin, end = inp.split(' ')[0], inp.split(' ')[1]
			begin_date = datetime.datetime.strptime(begin, '%Y-%m-%d').date() # inclusive 
			end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date() # inclusive 
			if end_date < begin_date:
				return None
			return [begin, end]
		except:
			return None

	inp = input('Enter a specific time period (format: YYYY-MM-DD YYYY-MM-DD (start and end dates, inclusive)). Type BACK to go back.\n> ')
	if inp == 'BACK':
		return
	dates = parse_input(inp)
	if dates is None:
		print('Invalid entry.')
		time_period()
	begin, end = dates[0], dates[1]
	days = pd.Series(pd.date_range(begin, end).format()).tolist()
	df_t = df.loc[df['Y-M-D'].isin(days)]
	if df_t.empty:
		print('No data for this time')
		time_period()
	analyze(df_t, begin, end, len(days))


def actcat_analysis(actcat, aggfunc):

	thing = input('Enter a(n) ' + actcat + '. Type BACK to go back.\n> ')
	if thing == 'BACK':
		return
	for period in time_periods:
		# group by period and thing, add ranking
		df2 = df.groupby([period, actcat]).agg(aggfunc).sort_values(by=cols['dur'], ascending=False)
		df2['Period rank'] = df2.groupby(level=0)[cols['dur']].rank(ascending=False)
		df2 = df2.reset_index()

		total_time = df2.groupby(period).agg({cols['dur']: 'sum'})
		df2 = df2.loc[df2[actcat] == thing]
		if df2.empty:
			print('Does not exist.')
			actcat_analysis(actcat, aggfunc)

		spec_dir = ''
		if actcat == cols['cat']:
			spec_dir = category_dir + thing + '/'
			top_act = df.groupby([period, cols['act']]).agg(agg_func).sort_values(by=cols['dur'], ascending=False)
			top_act = top_act.loc[top_act[cols['cat']] == thing]
			if top_act.empty:
				print('Does not exist.')
				actcat_analysis(actcat, aggfunc)
			top_act = top_act.reset_index()
			top_act = top_act.groupby([period, cols['cat']]).agg({cols['dur']: [first, second, third], cols['act']: [first, second, third]})

			top_act.columns = top_act.columns.get_level_values(0)
			top_act.columns = ['Top HMS', '2nd HMS', '3rd HMS', 'Top Activity', '2nd Activity', '3rd Activity']
			for col in ['Top HMS', '2nd HMS', '3rd HMS']:
				top_act[col] = top_act.apply(lambda row: s2hms(row[col]), axis=1)
			top_act = top_act[['Top Activity', 'Top HMS', '2nd Activity', '2nd HMS', '3rd Activity', '3rd HMS']]

			df2 = df2.rename({cols['dur']: 'Category time'}, axis=1)
			df2 = pd.merge(df2, top_act, on=period)

		else:
			spec_dir = activity_dir + thing + '/'
			df2 = df2.rename({cols['dur']: 'Activity time'}, axis=1)
		
		if not os.path.exists(spec_dir): os.makedirs(spec_dir)

		df2 = pd.merge(df2, total_time, on=period)
		df2['% Period'] = 100 * df2[actcat + ' time'] / df2[cols['dur']]

		# plotting!!!
		df2 = df2.sort_values(by=period)
		new = df2.copy()
		new[actcat + ' time'] = new[actcat + ' time'] / 3600
		new['Total time'] = new[cols['dur']] / 3600
		plt.cla()
		ax = plt.gca()
		new.plot(kind='line', x=period, y=actcat + ' time', ax=ax)
		new.plot(kind='line', x=period, y='Total time', ax=ax)
		#ax2 = ax.twinx()
		#new.plot(kind='line', x=period, y='% Period', ax=ax2)
		ax.set_ylabel("# Hours")
		ax.set_ylim(bottom=0)
		#ax.set_ylabel("% Period")
		#ax.set_ylim(bottom=0)
		plt.savefig(spec_dir + period + '_trend.png')


		# sort, convert to hms
		df2 = df2.sort_values(by=actcat + ' time', ascending=False)
		df2['Total period'] = df2.apply(lambda row: s2hms(row[cols['dur']]), axis=1)
		df2[actcat + ' time'] = df2.apply(lambda row: s2hms(row[actcat + ' time']), axis=1)

		# move columns, set index, change type
		if actcat == cols['cat']:
			df2 = df2[[period, actcat + ' time', 'Total period', '% Period', 'Period rank', 'Top Activity', 'Top HMS', '2nd Activity', '2nd HMS', '3rd Activity', '3rd HMS']]
		elif actcat == cols['act']:
			df2 = df2[[period, actcat + ' time', 'Total period', '% Period', 'Period rank']]
		df2 = df2.set_index(period)
		df2 = df2.astype({"Period rank": int})

		# save to file
		if actcat == cols['act']: 
			df2.to_csv(activity_dir + thing + '/' + period + '.csv', encoding='utf-8')
		elif actcat == cols['cat']: 
			df2.to_csv(category_dir + thing + '/' + period + '.csv', encoding='utf-8')

		print('Time period: ' + period)
		print(df2.head(50))
		print()


def get_inputs():
	inp = input('Type 1 for time period analysis.\nType 2 for activity analysis.\nType 3 for category analysis\n> ')
	while(inp != 'EXIT'):
		if inp == '1': 
			time_period()
		elif inp == '2': 
			actcat_analysis(cols['act'], agg_func)
		elif inp == '3': 
			actcat_analysis(cols['cat'], {cols['dur']: 'sum'})
		print('\n'*20)
		inp = input('Type 1 for time period analysis.\nType 2 for activity analysis.\nType 3 for category analysis\n> ')

get_inputs()















































