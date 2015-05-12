var fs = require('fs');
var poolModule = require('generic-pool');
var pool = poolModule.Pool({
  name: 'redis',
  create: function(callback){
    var cli = require('redis').createClient();
    callback(null, cli);
  },
  destroy: function(client){
    client.quit();
  },
  max: 1000,
  min: 2,
  refreshIdle: false,
  idleTimeoutMillis : 30000,
  log: false
});
/*
var client = new elasticsearch.Client({
    host: 'localhost:9200',
    log: 'warning',
    //log: 'trace',
  }
);
*/
var stockIdPrefix = 'TW';
var redis = require('redis');
var cli = redis.createClient();

cli.on('error', function(err){
  console.log('redis error:' + err);
});

var history = {};

var pm3 = 15 * 60 * 60 * 1000;
var day_width = 60 * 60 * 24 * 1000;
var start_ts = new Date("2004/02/11").getTime();
//var start_ts = new Date("2015/01/01").getTime();
//var stop_ts = new Date("2015/01/01").getTime();
var stop_ts = new Date().getTime() - day_width;

function twoDigit(a)
{
  if(a < 10)
    return '0' + a.toString();
  else
    return a.toString();
}

//var data = '';
while(start_ts < stop_ts){
  var day = new Date(start_ts);
  var Month = day.getMonth() + 1 ;
  var Day = day.getDate();
  var file_name = 'data/'+ day.getFullYear().toString() + twoDigit(Month) + twoDigit(Day) +'.csv';
  daystr = day.getFullYear().toString() + '-' + twoDigit(Month)+'-' + twoDigit(Day);
  console.log(file_name);
  start_ts += day_width;
  //Get necessary date data and start parse csv file
  var data = fs.readFileSync(file_name);
  if(data){
  //console.log(data);
      var array = data.toString().split('\n');
      for (i in array){
        var str = array[i];
        data = str.split('","');
        if(data.length == 16){
          var stock ={};
          var head = data[0].split('"');
          var stock_id = '';
          if(head.length == 2){
            stock_id = stockIdPrefix + head[1].trim();
          }else{
            stock_id = stockIdPrefix + head[0].trim();
          }
          //stock.id = stock_id;
          stock.volume = parseInt(data[2]);
          stock.open = parseFloat(data[5]);
          if(isNaN(stock.open)){
            stock.open = -1;
          }
          stock.high = parseFloat(data[6]);
          if(isNaN(stock.high)){
            stock.high = -1;
          }
          stock.low = parseFloat(data[7]);
          if(isNaN(stock.low)){
            stock.low = -1;
          }
          stock.val = parseFloat(data[8]);
          if(isNaN(stock.val)){
            stock.val = -1;
          }
          stock.date = daystr;
          stock.per = parseFloat(data[15]);
          stock.buyQuantity = parseInt(data[12]);
          stock.buyPrice = parseInt(data[11]);
          stock.saleQuantity = parseInt(data[14]);
          stock.salePrice = parseInt(data[13]);
          if(!stock.buyQuantity) stock.buyQuantity = 0;
          if(!stock.saleQuantity) stock.saleQuantity = 0;
          if(stock.val != -1){
            if(history[stock_id]){
              history[stock_id].push(stock);
            }else{
              history[stock_id] = [];
              history[stock_id].push(stock);
            }
            //console.log(stock);
          }
        }
      }
  }else{
    console.log(file_name + ' not exist?');
  }
}
var total = 0;
var added = 0;
for(i in history)
{
  total++;
  //console.log(i);
  pool.acquire(function(err, client){
    client.set(i, JSON.stringify(history[i]), function(err, res){
      added++;
      if(added == total){
        console.log("Import to Redis done");
      }
      pool.release(client);
    });
  });
}
