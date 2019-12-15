import pandas as pd
import os 

date_column="DATE"

def removable_columns():
    var=["SC_CODE","SC_GROUP", "SC_TYPE", "SC_NAME"]
    return var


def convert_keys_to_string(keys):
    string_var="("
    for item in keys:
        string_var=string_var+str(item) + ", " 
    string_var=string_var[:-2]
    string_var=string_var + " )"
    return string_var


def convert_keys_to_string_key(keys):
    string_var="("
    for item in keys:
        string_var=string_var+":"+str(item) + ", " 
    string_var=string_var[:-2]
    string_var=string_var + " )"
    return string_var


def get_date(_string1):
    date_string=_string1[3:9]
    var_temp=pd.to_datetime(date_string, format = "%d%m%y")
    date_string=str(var_temp.date())
    return date_string


def prepare_dict(dict_var,filename):
    dict_var[date_column]=get_date(os.path.basename(filename))
    item_removables=removable_columns()
    for elem in item_removables:
        result=dict_var.pop(elem, None)
    dict_var["TDCLOINDI"]=str(dict_var["TDCLOINDI"]) 
    dict_var["NO_TRADES"]=int(dict_var["NO_TRADES"])
    dict_var["NO_OF_SHRS"]=int(dict_var["NO_OF_SHRS"])
    dict_var["NET_TURNOV"]=int(dict_var["NET_TURNOV"])
    return dict_var

def url_date(date):
	str_var=""
	split_list=date.split("-")
	for idx in range(1,(len(split_list))):
		str_var= str_var + str(split_list[-idx])
	str_var=str_var+split_list[0][2:]
	return str_var


base_url={"BSE": 'https://www.bseindia.com/download/BhavCopy/Equity/', }
prefix={"BSE": "EQ",}
suffix={"BSE": "_CSV.ZIP",}
 
def url_create (exchange, date):
    url=base_url[exchange]+prefix[exchange]+url_date(date)+suffix[exchange]
    return url

dir_path= os.path.dirname(os.path.realpath(__file__))
base_folder=dir_path+"/zip_files2/"
def zip_name(exchange,date):
    name=base_folder+exchange+url_date(date)+suffix[exchange]
    return name

def csv_name_path(exchange,date):
    name=base_folder+exchange+url_date(date)+".CSV"
    return name

def date_range(date_start, date_end):
    a=list(pd.date_range(start=date_start,end=date_end, freq="d").date)
    return a

