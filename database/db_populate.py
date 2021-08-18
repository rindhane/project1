#! /usr/bin/env python
from .db_handlers import (
                          #BSE_DB,
                          BSE_DB_cloud,
                          #BSEstockEntry,
                          BSEstockEntryNew, 
                                )
from .downloader import (download_data,
                        exchange_default as EXCHANGE)
from .helper_file import date_range
import os 
import datetime as dt
import concurrent.futures as lib
from secrets.db_creds import Creds
import logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

#equity_storage_path
dir_path= os.path.dirname(os.path.realpath(__file__))
DB_XPATH=dir_path+"/equity_db.db"
DB_CRED=Creds()
#DB_CRED.db_path=DB_XPATH
db=BSE_DB_cloud(**vars(DB_CRED))

def push_new_entries_archive(df,db_object,entryClass,):
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

def push_new_entriesScript(df,db_object,entryClass):
        script=entryClass.get_execution_insertScript(df)
        return db_object.execute_script(script)

def push_new_entries(df,db_object,entryClass,):
        for stock in df.iloc :
                #obtain insert statement for single stock and excute in the
                #database
                statement=entryClass.get_execution_insert(stock)  
                insert_status=db_object.execute_script(statement)
        return True

def push_new_table(df,db_object,entryClass):
        #get tables not present in db  
        tables=db_object.tables_not_available(
                df[entryClass.security_TABLE])
        #push table in db
        heads=entryClass.get_indicator_keys(o='create')
        for table in tables:
                db_object.create_table(str(table),heads)
        return True
        
def populate_engine_archive(db_class,db_cred,entryClass,
                start_date,end_date,
                exchange,
                workers=None,threads=None,):
        #dates expected in iso format
        date_iterator=date_range(start_date,end_date)
        #initalization database
        db_object=db_class(**vars(db_cred))
        cursor=db_object.initiate_connection()
        logging.info("State of program %s", 'start')
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
                                logging.info("Date:%s , finished entry ", date.isoformat())
                        #--common final entry---#
                        db_object.insert_date(date,status)
                        cursor.connection.commit()
        db_object.close_connection()
        logging.info("State of program %s", 'start') 
        return db_object

def single_thread_DB_IO (df,date,db_class,db_cred,
                        entryClass,status=1):
        #it is assumed to be on the df is not null and have values
        #also asuumed date is not available in database
        db_object=db_class(**vars(db_cred))#need cred object here
        cursor=db_object.initiate_connection()
        push_new_table(df,db_object,entryClass)
        push_new_entries(df,db_object,entryClass)
        db_object.insert_date(date,status)
        db_object.close_connection()
        return True

def multi_thread_DB_IO(func,df,date,db_class,
                 db_cred,entryClass,workers,threads,status=1):
        #func is single thread DB_IO
        block=int(len(df)/threads)+1
        with lib.ThreadPoolExecutor(max_workers=workers) as executor:
                for i in range(0,threads):
                        df_thread=df[i*block:(i+1)*block]
                        executor.submit(func,df_thread,date,db_class,db_cred,entryClass,status=status)
        logging.info("Date:%s , finished entry ", date.isoformat())
        return True

def populate_single_date(db_class,db_cred,date,
                        entryClass,exchange,
                        workers,
                        threads):
        #initalization entry
        db_object=db_class(**vars(db_cred))
        cursor=db_object.initiate_connection()
        if not db_object.isDate(date):
                df=download_data(date=date,exchange=exchange)
                # initalize status flag
                status=1
                if df is None:
                        status=0
                #handling further if data
                if status == 1 :
                        multi_thread_DB_IO(
                                single_thread_DB_IO,
                                df,
                                date,
                                db_class,
                                db_cred,
                                entryClass,
                                workers=workers,
                                threads=threads,
                                status=status,
                        )
                #--common final entry---#
                db_object.insert_date(date,status)
                cursor.connection.commit()
        db_object.close_connection() 
        return db_object

def populate_engine_multiThread(db_class,db_cred, entryClass,
                                start_date,end_date,
                                exchange,
                                workers=5,
                                threads=100,
                                ):
        #dates expected in iso format
        date_iterator=date_range(start_date,end_date)
        logging.info("State of program %s", 'start')
        for date in date_iterator:
                populate_single_date(
                        db_class=db_class,
                        db_cred=db_cred,
                        date=date,
                        entryClass=entryClass,
                        exchange=exchange,
                        workers=workers,threads=threads,
                )
        logging.info("State of program %s", 'end')
        return True

if __name__=='__main__':
        try:
                #creating date table if it doesn't exist
                db.create_date_table(cls=BSEstockEntryNew)
        except:
                pass
        #initalization inputs
        WORKERS=10
        THREADS=100
        start_date=dt.date(day=1,month=1,year=2007).isoformat()
        end_date=dt.date.today().isoformat()
        populate_engine_multiThread(BSE_DB_cloud,DB_CRED,BSEstockEntryNew,
                start_date,end_date,
                exchange=EXCHANGE,
                workers=WORKERS,
                threads=THREADS,
        )
        