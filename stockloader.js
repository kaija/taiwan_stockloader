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

//start time
var start_ts = new Date("2015/04/30").getTime()
//end time
var stop_ts = new Date().getTime() - day_diff; //Not download today

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
		var file_str = 'data/' + fullYear + twoDigit(tw_month) + twoDigit(tw_day)+'.csv';
		var data = {file: file_str, body:''};
		httpreq.post('http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php',{
			parameters:{
				download: 'csv',
				qdate: date_str,
				selectType: 'ALLBUT0999'
			},
			binary: true
		}, function(err, res){
			if(err) {
				console.log(err)
			}else{
				data.body = res.body;
				fullfill(data);
			}
		});
/*
		var options = {
			hostname:'www.tse.com.tw',
			port: 80,
			path:'/ch/trading/exchange/MI_INDEX/MI_INDEX.php',
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
				'Content-Length': postData.length
			}
		};
		var req = http.request(options, function(res){
			res.setEncoding('binary');
			var data = {file:file_str, body:''};
			var body = '';
			res.on('data', function(chunk){
				//console.log(chunk);
				body+=chunk;
			});
			res.on('end', function(){
				data.body = body;
				fullfill(data);
			});
		});
		req.write(postData);
		req.end();
*/
	});
}

while(start_ts < stop_ts){
	downloadStock(start_ts).then(saveStock);
	start_ts += day_diff;
}
