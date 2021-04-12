//File responsible for making connection with the BSE server 



const https = require('https');
const http = require('http');
const fs = require('fs');
const fetch = require('node-fetch');
//const { Http2ServerRequest } = require('node:http2');


const options_trial = {
    hostname: 'api.bseindia.com',
    port: 443,
    path: '/BseIndiaAPI/api/StockReachGraph/w?scripcode=500111&flag=0&fromdate=&todate=&seriesid=',
    method: "GET"

}

const url='http://'+options_trial.hostname+options_trial.path;
//console.log(url);

module.exports=fetch; 

/*
http.get(url,res=>{
    process.stdout.write(res);
    res.on('data',(chunk)=>{
        process.stdout.write(chunk)
    })
}).on('error', (e)=>{
    console.log("error",e);
})*/





/*
const req=https.request(options_trial, (res)=>{
    console.log(`Status: ${res.statusCode}`,);
    res.on('Data', d=>{
        process.stdout.write(d)
    });
})

req.on('error',e=>{
    console.error(e);
})

req.end;

*/
