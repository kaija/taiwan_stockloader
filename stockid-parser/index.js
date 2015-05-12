var fs = require('fs');
var esIndex = 'stock';
var esType = 'stockname';
var elasticsearch = require('elasticsearch');
var poolModule = require('generic-pool');
var pool = poolModule.Pool({
  name:'elasticsearch',
  create: function(callback){
    var cli = new elasticsearch.Client({
      host:'localhost:9200',
      log: 'trace'
    });
    callback(null, cli);
  },
  destroy: function(client){
  },
  min: 100,
  max: 1000,
  refreshIdle: false,
  log: false
});

var stocklist = [];

var raw = fs.readFileSync('stocklist.txt');
if(raw){
  var rows = raw.toString().split('\n');
  for(i in rows){
    var line = rows[i].split(',');
    var id = line[0].trim();
    var name = line[1];
    var cat = line[5];
    if(id.length > 0){
      var stock = {};
      stock['id'] = id;
      stock['name'] = name;
      stock['category'] = cat;
      stocklist.push(stock);
    }
  }
}


for (j in stocklist){
  //console.log(stocklist[i]);
  pool.acquire(function(err, cli){
    var o = {
      index: esIndex,
      type: esType,
      body: stocklist[j]
    };
    console.log(o);
    cli.create(o, function(err, res){
      //console.log(stocklist[j].id + " save to ES");
      //console.log(res);
      pool.release(cli);
    });
  });
}

