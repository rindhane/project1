#! /usr/bin/env python
from .db_handlers import (
                          BSE_DB,
                          BSEstockEntry, 
                                )
from .downloader import (download_data,
                        exchange_default as exchange)
from .helper_file import date_range
import os 
import datetime as dt

#equity_storage_path
dir_path= os.path.dirname(os.path.realpath(__file__))
DB_PATH=dir_path+"/equity_db.db"
db=BSE_DB(db_path=DB_PATH)

def push_new_entries(df,db_object,entryClass):
        for stock in df.iloc :  
                entry=entryClass(**stock) #class to handle the columns to table headers
                #values for insert statement execution
                table= entry['TABLE']
                #expected columns
                headers=' , '.join(entry.get_indicator_keys())
                #values for columns
                values=entry.get_indicator_vals()
                values=entry.get_indicator_vals_string()
                #executing insert statement into database_object 
                insert_status=db_object.insert_row(table, headers,values,)
        return True

def push_new_table(df,db_object,entryClass):
        #get tables not present in db  
        tables=db_object.tables_not_available(
                df[entryClass.security_TABLE])
        #push table in db
        heads=' , '.join(entryClass().get_indicator_keys())
        for table in tables:
                db_object.create_table(str(table),heads)
        return True
        
def populate_engine(db_object,entryClass,
                start_date,end_date,
                exchange):
        #dates expected in iso format
        date_iterator=date_range(start_date,end_date)
        #initalization entry
        cursor=db_object.initiate_connection()
        for date in date_iterator:
                if not db_object.isDate(date):
                        df=download_data(date=date,exchange=exchange)
                        # initalize status flag
                        status=1
                        if df is None:
                                status=0
                        #handling further if data
                        if status == 1 :
                                push_new_table(df,db_object,entryClass)
                                push_new_entries(df,db_object,entryClass)
                        #--common final entry---#
                        db_object.insert_date(date,status)
                        cursor.connection.commit()
        db_object.close() 
        return db_object

if __name__=='__main__':
        try:
                #creating date table if it doesn't exist
                db.create_date_table()
        except:
                pass
        #initalization inputs
        start_date=dt.date(day=1,month=1,year=2007).isoformat()
        end_date=dt.date.today().isoformat()
        populate_engine(db,BSEstockEntry,
                start_date,end_date,
                exchange=exchange,
        )
        