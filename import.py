import datetime
import httplib
import urllib
import redis
import json
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

def convint(value):
	try:
		return int(value)
	except ValueError:
		return 0

today = datetime.date.today()
one_day = timedelta(days=1);

start_day = datetime.date(2004, 2, 11);
#start_day = datetime.date(2015, 1, 11);

print "Import from " + start_day.strftime("%Y-%m-%d") + " to " + today.strftime("%Y-%m-%d")

dl_date = start_day


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
			sid = head[1].strip(" ")
			#print head[1] + " " + r[2] + " " + convfloat(r[5])
			#print r[2] #volume
			#print r[5] #open
			if sid in stocks:
				stocks[sid].append({"volume": convint(r[2]), "open": convfloat(r[5]), "high": convfloat(r[6]), "low": convfloat(r[7]), "val": convfloat(r[8]), "date": dl_date.strftime("%Y-%m-%d"), "per": convfloat(r[15]), "buyQuantity": convint(r[12]), "buyPrice": convint(r[11]), "saleQuantity": convint(r[14]), "salePrice": convint(r[13])})
			else:
				stocks[sid] = []
				stocks[sid].append({"volume": convint(r[2]), "open": convfloat(r[5]), "high": convfloat(r[6]), "low": convfloat(r[7]), "val": convfloat(r[8]), "date": dl_date.strftime("%Y-%m-%d"), "per": convfloat(r[15]), "buyQuantity": convint(r[12]), "buyPrice": convint(r[11]), "saleQuantity": convint(r[14]), "salePrice": convint(r[13])})

	dl_date += one_day

print "Start import to Redis"


rdb = redis.Redis('localhost')
for i in iter(stocks):
	sid = "TW" + i
	rdb.set(sid, json.dumps(stocks[i]))
