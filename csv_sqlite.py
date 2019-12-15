import pandas as pd
import sqlite3
import helper_file
import db_functions

#filename="EQ010719.CSV"
db_name_location="equity_db.db"
sec_code="SC_CODE"
exchange_code={"BSE":"B"}

#Making connection with the data base 
def initiate_connection(db_location=db_name_location):
        db=sqlite3.connect(db_location)
        cursor=db.cursor()
        return cursor, db



def csv_to_sqlite(file_var, exchange, cursor):
        file1=pd.read_csv(file_var)
        for i in range(0,len(file1)):  
                dict_row=dict(file1.iloc[i]) #dictionary variable to insert in the table
                var_table= exchange_code[exchange] + str(dict_row[sec_code]) #preparing table variable
                dict_row=helper_file.prepare_dict(dict_row,file_var)#prepare dict_row variable as per the table schema 
                insert_status=db_functions.insert_row(var_table, dict_row ,cursor) # inserting row into table
        return insert_status

#csv_to_sqlite(filename,exchange_name)
#db.commit()
#db.close()