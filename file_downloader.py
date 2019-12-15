import requests
from helper_file import url_create, zip_name, csv_name_path, date_range
from zipfile import ZipFile
import pandas as pd 
from csv_sqlite import csv_to_sqlite ,initiate_connection
from db_functions import update_date_record



def write_zip(zip_file,request):
	with open(zip_file, 'wb') as f:
		f.write(request.content)

def write_csv(zip_file,csv_name):
	with ZipFile(zip_file,"r") as zf:
		with open(csv_name,"wb") as c:
			c.write(zf.read(zf.namelist()[0]))

  



def download_csv_files(start_date,end_date,exchange=exchange_default):
	print('Beginning download ')
	date_list=date_range(start_date,end_date)
	error_date=list()
	for items in date_list:
		date_var=str(items)
		url_trial=url_create(exchange_default,date_var)
		r = requests.get(url_trial, proxies=proxies )
		try:
			if r.status_code==200 and r.headers['content-type']=="application/x-zip-compressed":
				zip_file=zip_name(exchange,date_var)
				print(date_var)
				write_zip(zip_file,r)
				csv_name=csv_name_path(exchange,date_var)
				write_csv(zip_file,csv_name)
				status=csv_to_sqlite(csv_name,exchange,cursor)
				if status==True:
					update_date_record(cursor,date_var,r.status_code)
			else:
				raise ValueError("No zip file")
		except ValueError:
			update_date_record(cursor,date_var,r.status_code)#error_date.append(items)
	print("Download complete")


if __name__= "__main__":
	#initialization inputs
	exchange_default="BSE"
	start_date = "2007-01-01"
	end_date= "2019-08-09"
	proxies = {"http": "http://rahuli:passQ@1234@10.3.3.139:3128", 
            "https": "https://rahuli:passQ@1234@10.3.3.139:3128"   } 
	#starting the program
	cursor, db = initiate_connection()
	download_csv_files(exchange=exchange_default,start_date=start_date,end_date=end_date)
	db.commit()
	db.close()
