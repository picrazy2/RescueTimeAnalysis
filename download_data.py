from datetime import timedelta, date, datetime
import os, csv, requests, sys

base = 'https://www.rescuetime.com/anapi/data?'
key = 'B63bUhh7mec7rPLKDBbmmx3ohFNlIOGy7Wki5cRZ'
perspective = 'interval' # rank or interval
resolution_time = 'minute' # month, week, day, hour, or minute (minute is 5 min interval)
form = 'csv' # only works with csv rn
# there are other attributes, but we're not using them

start = datetime.strptime(sys.argv[1], '%Y-%m-%d').date() # inclusive 
end = datetime.strptime(sys.argv[2], '%Y-%m-%d').date() # inclusive

real_begin = date(2013, 1, 1)
real_end = date(2019, 7, 30)

file_location = 'data/'

def create_string(base, key, attrs):
    ret = base + 'key=' + key + '&'
    for key in attrs:
            ret = ret + key + '=' + attrs[key] + '&' if attrs[key] != None else ret
    return ret[:-1] if ret[-1] == '&' else ret

attrs = {'perspective': perspective, 'resolution_time': resolution_time,'format': form}
dates = [(start + timedelta(n)).strftime("%Y-%m-%d") for n in range(int((end - start).days) + 1)]
print('Total ' + str(len(dates)) + ' dates')

if start > end or start < real_begin or end > real_end:
    sys.exit('date range invalid')

if not os.path.exists(file_location):
    os.makedirs(file_location)

for i, day in enumerate(dates):
    attrs.update({'restrict_begin': day, 'restrict_end': day})
    with open(file_location + day + '.' + form, 'w') as f:
        with requests.Session() as s:
            download = s.get(create_string(base, key, attrs))
            decoded_content = download.content.decode('utf-8')
            cr = list(csv.reader(decoded_content.splitlines(), delimiter=','))
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in cr:
                writer.writerow(row)

    if (i+1) % 100 == 0:
        print(str(i+1) + ' days downloaded')

print('Done')