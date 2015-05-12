var fs = require('fs');
var raw = fs.readFileSync('stocklist.txt');
if(raw){
  var rows = raw.toString().split('\n');
  for(var i in rows){
    var line = rows[i].split(',');
    var id = line[0].trim();
    var name = line[1];
    var cat = line[5];
    if(id.length > 0){
      var stock = {};
      stock['id'] = id;
      stock['name'] = name;
      stock['category'] = cat;
      console.log(stock);
    }
  }
}
