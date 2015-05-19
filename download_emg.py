#!/usr/bin/python
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

start_day = datetime.date(2007, 7, 1);

print "Download from " + start_day.strftime("%Y-%m-%d") + " to " + today.strftime("%Y-%m-%d")

dl_date = start_day



while dl_date < today:
	httpreq = httplib.HTTPConnection('www.tpex.org.tw')
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	date_str = str(dl_date.year - 1911 ) + dl_date.strftime("/%m/%d")
	#http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=
	url = "/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=" + date_str+ "&s=0,asc,0"
	httpreq.request("GET", url, "", headers);
	httpres =  httpreq.getresponse()
	stock_csv =  httpres.read()
	file_name = "emerging/" + dl_date.strftime("%Y%m%d") + ".csv"
	print "downloading " + file_name
	f = open(file_name, "w")
	f.write(stock_csv)
	dl_date += one_day


print "Download Finish!"

