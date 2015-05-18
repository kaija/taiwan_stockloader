from elasticsearch import Elasticsearch

def import_stock_id(client, sid, name, cat, stype):
  return client.create(
    index= 'stock',
    doc_type= 'stockname',
    body = {
      'id': sid,
      'name': name,
      'category': cat,
      'type': stype
    }
  )


es = Elasticsearch()

#print import_stock_id(es, 'test', 'test', 'test')

f = open('stocklist-em.txt', 'r')
lines = f.readlines()
for line in lines:
  r = line.split(',')
  print import_stock_id(es, r[0], r[1], r[5], 'emerging')
  #print r[0] + ':' + r[1] + ':' + r[5]

f = open('stocklist.txt', 'r')
lines = f.readlines()
for line in lines:
  r = line.split(',')
  print import_stock_id(es, r[0], r[1], r[5], "")
