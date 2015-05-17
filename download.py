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

