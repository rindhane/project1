from utilities.data_analysis import ( Source_sqlite,Source_Json)
import pandas as pd
import os
import numpy as np                                    
#---------constants--------------
DATA1=os.path.dirname(__file__)+'/equityBSE.db'
DATA2=os.path.dirname(__file__)+'/tables.json'
#-----------------------
#derived parameters
sources= {
    'stocks':Source_sqlite(name='stocks',path=DATA1)
    #'tables':Source_
}

keys= {
    'codes':Source_Json(name='codes',path=DATA2)
}
#-----------------

COLUMNS_DICT= {
    'DATE': [pd.Timestamp],
    'OPEN': [lambda x: float(x)], 
    'HIGH': [lambda x: float(x)], 
    'LOW':  [lambda x: float(x)], 
    'CLOSE': [lambda x: float(x)],  
    'LAST': [lambda x: float(x)], 
    'PREVCLOSE': [lambda x: float(x)], 
    'NO_TRADES':[lambda x: float(x)],
    'NO_OF_SHRS':[lambda x: float(x)],
    'NET_TURNOV':[lambda x: float(x)],
    'TDCLOINDI':[lambda x: (np.nan if x=='nan' else x)],
 }

def processor(col, schema):
    details= schema[col.name]
    return col.apply(details[0], **(details[1] if details[1:] else {}))

def process_nothing(col):
    return col

def cleaner(result,cols=COLUMNS_DICT.keys(),sorter=['DATE']):
    #remark: does dictionary{COLUMNS_DICT.keys()} always provide keys in the same order
    df=pd.DataFrame(result,columns=cols,copy=True)
    if sorter is not None:
        df=df.sort_values(by=sorter)
    df=df.reset_index(drop=True)
    return df

def pre_processing(df,process_dict=COLUMNS_DICT,**kwargs):
    df=df.apply(processor, **{'schema':process_dict})
    return df
