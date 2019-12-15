import os
import sqlite3  
from helper_file import csv_name_path
from csv_sqlite import initiate_connection,csv_to_sqlite


exchange ="BSE"
cursor, db = initiate_connection()
path=csv_name_path(exchange,"2018-06-05")
csv_to_sqlite(path,exchange,cursor)

db.commit()
db.close()


if __name__ == "__main__":
    print("fThis is a trial file")
    #print(type(r.status_code)) # Retrieve HTTP meta-data
    #print(type(r.headers['content-type']))
    #print(type(r.encoding))