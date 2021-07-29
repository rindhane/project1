import pandas as pd
from database.db_populate import ( db,
                                  exchange,
                                 )
def data_to_pandas(scrip):
    scrip=exchange+str(scrip)
    curr=db.get_cursor()
    data=pd.read_sql_query(f"SELECT * from {scrip}",curr.connection)
    data=data[~data.duplicated(subset="DATE")]
    data['DATE']=pd.to_datetime(data["DATE"])
    data=data.sort_values(by=["DATE"])
    #data=data.reset_index()
    #data=data.drop(columns=["index"])
    db.close_connection() 
    return data









