import datetime
import httplib
import urllib
from datetime import timedelta

#now = datetime.datetime.now();
#today = now.strftime('%Y-%m-%d')
#print today

today = datetime.date.today()
one_day = timedelta(days=1);

#start_day = datetime.date(2004, 2, 11);
start_day = datetime.date(2015, 5, 1);

print "Download from " + start_day.strftime("%Y-%m-%d") + " to " + today.strftime("%Y-%m-%d")

dl_date = start_day

httpreq = httplib.HTTPConnection('www.twse.com.tw')
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}


while dl_date < today:
	date_str = dl_date.strftime("%Y-%m-%d")
	form = urllib.urlencode({'download': 'csv', 'qdate': date_str, 'selectType': 'ALLBUT0999'})
	httpreq.request("POST", "/ch/trading/exchange/MI_INDEX/MI_INDEX.php", form, headers);
	httpres =  httpreq.getresponse()
	stock_csv =  httpres.read()
	file_name = "data/" + dl_date.strftime("%Y%m%d") + ".csv"
	print "downloading " + file_name
	file = open(file_name, "w")
	file.write(stock_csv)
	dl_date += one_day


