from datetime import timedelta, date
import os, csv, requests

base = 'https://www.rescuetime.com/anapi/data?'
key = 'B63bUhh7mec7rPLKDBbmmx3ohFNlIOGy7Wki5cRZ'
perspective = 'interval' # rank or interval
resolution_time = 'minute' # month, week, day, hour, or minute (minute is 5 min interval)
form = 'csv' # only works with csv rn

start = date(2013, 1, 1) # inclusive
end = date(2019, 7, 9) # inclusive

file_location = 'data/'

def create_string(base, key, attrs):
    ret = base + 'key=' + key + '&'
    for key in attrs:
            ret = ret + key + '=' + attrs[key] + '&' if attrs[key] != None else ret
    return ret[:-1] if ret[-1] == '&' else ret

attrs = {'perspective': perspective, 'resolution_time': resolution_time,'format': form}
dates = [(start + timedelta(n)).strftime("%Y-%m-%d") for n in range(int((end - start).days) + 1)]
print('Total ' + str(len(dates)) + ' dates')

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

    if i > 0 and i % 100 == 0:
        print(str(i) + ' days downloaded')

print('Done')