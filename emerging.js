var http = require('http');
var fs = require('fs');
var querystring = require('querystring');
var Promise = require('promise');
var httpreq = require('httpreq');
console.log("Start download stock information...");
var day_diff = 60 * 60 * 24 * 1000;


if(!fs.existsSync('data')){
	fs.mkdirSync('data');
}

//Emerging stock only start from 2007/07/01
var start_ts = new Date("2007/07/01").getTime();
//var start_ts = new Date("2015/01/01").getTime()
//end time
var stop_ts = new Date().getTime() - day_diff; //Not download today
//var stop_ts = new Date("2015/05/12").getTime()

function twoDigit(num)
{
	if(num < 10){
		return '0' + num;
	}
	return num;
}

function saveStock(data)
{
	//console.log("Date:" + data.body);
	fs.writeFile(data.file, data.body,function(err){
		if(err){
			console.log(err);
		}else{
			console.log("File " + data.file + " download.");
		}
	});
}

function downloadStock(start_ts)
{
	var date = new Date(start_ts);
	return new Promise(function(fullfill, reject){
		var tw_year = date.getFullYear() - 1911;
		var tw_month =  date.getMonth() + 1;
		var tw_day = date.getDate();
		var date_str = tw_year.toString() + '/' + twoDigit(tw_month) + '/' + twoDigit(tw_day);
		var fullYear = date.getFullYear().toString();
		var file_str = 'data/em' + fullYear + twoDigit(tw_month) + twoDigit(tw_day)+'.csv';
		var data = {file: file_str, body:''};
    //http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=104/05/12&s=0,asc,0
    var qstr = "http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=" + date_str+"&s=0,asc,0";
		httpreq.post(qstr,{
			binary: true
		}, function(err, res){
			if(err) {
				console.log(err)
			}else{
				data.body = res.body;
				fullfill(data);
			}
		});
	});
}

while(start_ts < stop_ts){
	downloadStock(start_ts).then(saveStock);
	start_ts += day_diff;
}
