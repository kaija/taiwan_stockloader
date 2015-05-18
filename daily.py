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


def save2redis(key, value):
	old = rdb.get("TW" + key)
	if old is None:
		val = []
		val.append(value)
		rdb.set("TW"+key ,json.dumps(val))
	else:
		l = json.loads(old)
		l.append(value)
		rdb.set("TW"+key ,json.dumps(l))


today = datetime.date.today()
one_day = timedelta(days=1)
dl_date = today

httpreq = httplib.HTTPConnection('www.twse.com.tw')
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
date_str = str(dl_date.year - 1911 ) + dl_date.strftime("/%m/%d")
form = urllib.urlencode({'download': 'csv', 'qdate': date_str, 'selectType': 'ALLBUT0999'})
httpreq.request("POST", "/ch/trading/exchange/MI_INDEX/MI_INDEX.php", form, headers);
httpres =  httpreq.getresponse()
stock_csv =  httpres.read()

lines = stock_csv.split("\n")
for line in lines:
	r = line.split('","')
	if len(r) == 16:
		head = r[0].split("\"")
		sid = head[1].strip(" ")
		obj = {"volume": convint(r[2]), "open": convfloat(r[5]), "high": convfloat(r[6]), "low": convfloat(r[7]), "val": convfloat(r[8]), "date": dl_date.strftime("%Y-%m-%d"), "per": convfloat(r[15]), "buyQuantity": convint(r[12]), "buyPrice": convint(r[11]), "saleQuantity": convint(r[14]), "salePrice": convint(r[13])}
		print sid
		print obj
		save2redis(sid, obj)
