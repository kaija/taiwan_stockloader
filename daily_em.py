#!/usr/bin/python
import datetime
import httplib
import urllib
import redis
import json
from datetime import timedelta

#now = datetime.datetime.now();
#today = now.strftime('%Y-%m-%d')
#print today
rdb = redis.Redis('localhost')

def rv(value):
	out = ""
	for num in value.strip().split(","):
		out+=num
	return out

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

def convint(value):
	try:
		return int(value)
	except ValueError:
		return 0

def dump(key, value):
	print key
	print json.dumps(value)

def save2redis(key, value):
	old = rdb.get("TWE" + key)
	if old is None:
		val = []
		val.append(value)
		rdb.set("TWE"+key ,json.dumps(val))
	else:
		l = json.loads(old)
		l.append(value)
		rdb.set("TWE"+key ,json.dumps(l))
		


today = datetime.date.today()
one_day = timedelta(days=1)
print "Download "
dl_date = today - one_day
#start_day = datetime.date(2015, 5, 14);
httpreq = httplib.HTTPConnection('www.tpex.org.tw')
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
date_str = str(dl_date.year - 1911 ) + dl_date.strftime("/%m/%d")
url = "/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=" + date_str+ "&s=0,asc,0"
httpreq.request("GET", url, "", headers);
httpres =  httpreq.getresponse()
stock_csv =  httpres.read()
#print stock_csv
print "Import " + today.strftime("%Y-%m-%d")

lines = stock_csv.split("\n")
for line in lines:
  r = line.split('","')
  if len(r) == 17:
    head = r[0].split("\"")
    sid = head[1].strip(" ")
    print sid
    obj = {"volume": convint(rv(r[8])), "open": convfloat(r[4]), "high": convfloat(r[5]), "low": convfloat(r[6]), "val": convfloat(r[2]), "date": dl_date.strftime("%Y-%m-%d"), "avg": convfloat(r[7]), "buyPrice": convfloat(r[11]), "salePrice": convfloat(r[12])}
    save2redis(sid, obj)
    #print obj

