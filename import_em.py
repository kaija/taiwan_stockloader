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
one_day = timedelta(days=1);

start_day = datetime.date(2015, 5, 14);
#start_day = datetime.date(2015, 5, 14);

print "Import from " + start_day.strftime("%Y-%m-%d") + " to " + today.strftime("%Y-%m-%d")

dl_date = start_day


stocks = {}

dl_date = start_day
print "Start merge history"

while dl_date < today:
	file_name = "emerging/" + dl_date.strftime("%Y%m%d") + ".csv"
	f = open(file_name, 'r')
	print "open " + file_name
	lines = f.readlines()
	for line in lines:
		r = line.split('","')
		if len(r) == 17:
			head = r[0].split("\"")
			sid = head[1].strip(" ")
			obj = {"volume": convint(rv(r[8])), "open": convfloat(r[4]), "high": convfloat(r[5]), "low": convfloat(r[6]), "val": convfloat(r[2]), "date": dl_date.strftime("%Y-%m-%d"), "avg": convfloat(r[7]), "buyPrice": convfloat(r[11]), "salePrice": convfloat(r[12])}
			dump(sid, obj)

	dl_date += one_day

