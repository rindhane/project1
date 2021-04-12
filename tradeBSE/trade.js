const transporter = require('./transporter');

url="http://api.bseindia.com/BseIndiaAPI/api/StockReachGraph/w?scripcode=500111&flag=0&fromdate=&todate=&seriesid="

transporter(url)
.then(res=>res.json())
.then(object=>sum_val(JSON.parse(object.Data)))
.catch(e=>console.log(e));




function sum_val(entries){
    let total = 0;
    entries.forEach(element => {
        total+=parseInt(element.vole);
    });
    console.log(total);
} 




