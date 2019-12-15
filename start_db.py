import sqlite3
import pandas as pd
from csv_sqlite import initiate_connection
from db_functions import table_structure


def data_to_pandas(scrip):
    #db_name_location="equity_db.db"
    curr, db = initiate_connection()
    scrip="B"+str(scrip)
    curr.execute(f"SELECT * from {scrip}")
    bse_table=table_structure()
    data=pd.DataFrame(curr.fetchall(),columns=bse_table.dict.keys())
    data=data[~data.duplicated(subset="DATE")]
    data.date=pd.to_datetime(data.DATE)
    data=data.sort_values(by=["DATE"])
    data=data.reset_index()
    data=data.drop(columns=["index"])
    db.close() 
    return data


#commands to run live check of the database is remaining
#curr.execute("SELECT * FROM sqlite_master")
#print(curr.fetchall())
#db.commit()
   






