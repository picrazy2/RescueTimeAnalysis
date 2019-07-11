import pandas as pd, time

all_data_location = 'all_data.csv'
cols = {'date': 'Date', 'dur': 'Time Spent (seconds)', 'people': 'Number of People', 'act': 'Activity', 'cat': 'Category', 'prod': 'Productivity'}
pd.options.display.max_rows = 100

def seconds_to_hms(seconds):
	return [seconds//3600, (seconds%3600)//60, seconds%60]

def seconds_to_hms_string(seconds):
	return ':'.join([str(x) for x in seconds_to_hms(seconds)])

def parse_date(date):
	spl = date.split('T')
	return [int(x) for x in spl[0].split('-') + spl[1].split(':')][:-1] #format is [Y, M, D, H, M]
	
def get_time_rank_for_year_act(act):
	ret = []
	for yr in years:
		if yr_act.index.isin([(yr, act)]).any():
			ret.append(yr_act.loc[yr, act][[cols['dur'], 'rank']])
		else:
			ret.append(pd.Series([0, -1], index=[cols['dur'], 'rank']))
	return ret

agg_func = {cols['dur']: 'sum', cols['cat']: 'first', cols['prod']: 'first'};


start = time.time()

df = pd.read_csv(all_data_location)
TOTAL_SECONDS = df[cols['dur']].sum()
TOTAL_HMS = seconds_to_hms(TOTAL_SECONDS)

# make year, month, day, hour, min columns
df['Year'], df['Month'], df['Day'], df['Hour'], df['Min'] = zip(*df[cols['date']].map(parse_date))
df = df[['Year', 'Month', 'Day', 'Hour', 'Min', cols['dur'], cols['act'], cols['cat'], cols['prod']]]
years = df['Year'].unique()

# group on year and activity, add rank
yr_act = df.groupby(['Year', cols['act']]).aggregate(agg_func).sort_values(by=cols['dur'], ascending=False)
yr_act['rank'] = yr_act.groupby(level=0)[cols['dur']].rank(ascending=False)

# group time by activity
all_time = df.groupby(df[cols['act']]).aggregate(agg_func).sort_values(by=cols['dur'], ascending=False).reset_index()
all_time.index += 1
all_time['H:M:S'] = all_time.apply(lambda row: seconds_to_hms_string(row[cols['dur']]), axis=1)
#all_time = all_time[[cols['act'], cols['dur'], 'H:M:S', cols['cat'], cols['prod']]]
all_time = all_time[[cols['act'], cols['dur'], 'H:M:S']]

# add year breakdowns
temp = list(zip(*all_time[cols['act']].map(get_time_rank_for_year_act)))
for i, year in enumerate(years):
	all_time[str(year) + ' (hms)'] = [seconds_to_hms_string(x[cols['dur']]) for x in temp[i]]

for i, year in enumerate(years):
	all_time[str(year) + ' (rank)'] = [int(x['rank']) if x['rank'] != -1 else '-' for x in temp[i]]

print(all_time.head(50))
print('Total time: ' + str(TOTAL_SECONDS) + ' seconds, or ' + seconds_to_hms_string(TOTAL_SECONDS))

print('Finished in ' + str(time.time() - start))