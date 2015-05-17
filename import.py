import datetime
import httplib
import urllib
from datetime import timedelta

#now = datetime.datetime.now();
#today = now.strftime('%Y-%m-%d')
#print today


def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

def convfloat(value):
	try:
		return float(value)
	except ValueError:
		return -1

today = datetime.date.today()
one_day = timedelta(days=1);

#start_day = datetime.date(2004, 2, 11);
start_day = datetime.date(2010, 8, 21);

print "Download from " + start_day.strftime("%Y-%m-%d") + " to " + today.strftime("%Y-%m-%d")

dl_date = start_day



while dl_date < today:
	httpreq = httplib.HTTPConnection('www.twse.com.tw')
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	date_str = str(dl_date.year - 1911 ) + dl_date.strftime("/%m/%d")
	form = urllib.urlencode({'download': 'csv', 'qdate': date_str, 'selectType': 'ALLBUT0999'})
	httpreq.request("POST", "/ch/trading/exchange/MI_INDEX/MI_INDEX.php", form, headers);
	httpres =  httpreq.getresponse()
	stock_csv =  httpres.read()
	file_name = "data/" + dl_date.strftime("%Y%m%d") + ".csv"
	print "downloading " + file_name
	f = open(file_name, "w")
	f.write(stock_csv)
	dl_date += one_day


print "Download Finish!"

stocks = {}

dl_date = start_day
print "Start merge history"

while dl_date < today:
	file_name = "data/" + dl_date.strftime("%Y%m%d") + ".csv"
	f = open(file_name, 'r')
	print "open " + file_name
	lines = f.readlines()
	for line in lines:
		r = line.split('","')
		if len(r) == 16:
			head = r[0].split("\"")
			sid = head[1]
			#print head[1] + " " + r[2] + " " + convfloat(r[5])
			#print r[2] #volume
			#print r[5] #open
			if sid in stocks:
				stocks[sid].append({'volume': r[2], 'open': convfloat(r[5]), 'high': convfloat(r[6]), 'low': convfloat(r[7]), 'val': convfloat(r[8]), 'date': dl_date.strftime("%Y-%m-%d"), 'per': convfloat(r[15])})
			else:
				stocks[sid] = []
				stocks[sid].append({'volume': r[2], 'open': convfloat(r[5]), 'high': convfloat(r[6]), 'low': convfloat(r[7]), 'val': convfloat(r[8]), 'date': dl_date.strftime("%Y-%m-%d"), 'per': convfloat(r[15])})

	dl_date += one_day

print "Start import to Redis"


for i in iter(stocks):
	print stocks[i]


