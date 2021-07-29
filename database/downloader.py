#! /usr/bin/env python
import pandas as pd
import requests
from io import BytesIO
import zipfile 
import datetime as dt

exchange_default="BSE"
exchange_url={
    'BSE-Equity-new':'https://www.bseindia.com/download/BhavCopy/Equity/EQ%s_CSV.ZIP',
    'BSE-Equity-old': 'https://www.bseindia.com/download/BhavCopy/Equity/eq%s_csv.zip',
}

headers={
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
}

def get_dataframe(_bytes):
    #_bytes should represent a zipfile in bytes
    zp=zipfile.ZipFile(file=BytesIO(_bytes))
    #obtaining csv_data from the zipfile 
    csv_file=BytesIO(zp.open(zp.namelist()[0]).read())
    return pd.read_csv(csv_file)

def url_create (exchange, date,exchange_url=exchange_url ,**kwargs):
    key=''
    if exchange=='BSE':
        key=key+exchange
        key=key+'-'+kwargs.get('type','Equity')
        key=key+'-'+ ('old' if date <=dt.date(day=27,month=3,year=2014) else 'new')
    url=exchange_url.get(key,None)
    if url==None:
        raise ValueError('inputs for url are not adequate')
    url=url% date.strftime('%d%m%y')
    return url

def get_response(date, exchange ,
                    proxies=None,
                    headers=headers,
                    url_creator=url_create,**kwargs):
    url=url_creator(exchange,date)
    r = requests.get(url, proxies=proxies ,headers=headers )
    if r.status_code==200 and r.headers['content-type']=="application/x-zip-compressed":
        return r.content
    return None 

def security_code_transformer(code,exchange):
    return str(exchange)+str(code)

def df_processor(col,exchange=exchange_default):
    if col.name=='SC_CODE':
        return col.apply(security_code_transformer,exchange=exchange)
    return col 

def download_data(date,exchange, 
                      processor=df_processor):
    if isinstance(date,str):
        date=dt.date.fromisoformat(date)
    print(f'Beginning download {str(date)}')
    #fetching the zip file from the exchange and stored in result in bytes type
    result=get_response(date=date,exchange=exchange)
    #segment to handle no data in response
    if result==None:
        print(date,"no data on this date")
        return None
    #segment handling the data in response
    #obtaining dataframe from the result 
    df=get_dataframe(result)
    #post-processing of df data
    df['DATE']=date
    df=df.apply(processor)
    print(f"Download complete {str(date)}")
    return df
    

if __name__== "__main__":
    #initialization input
    #dates in iso format
    check_date = "2019-08-01" 
    #starting the program
    result=download_data(exchange=exchange_default,date=check_date)
    print(result)
