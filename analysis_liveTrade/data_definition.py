from utilities.general.class_builders import self_setup_class
from utilities.data_analysis import ( 
                                        Data, 
                                        Source_Json)
                                            
import pandas
import os 
#---------constants--------------
DATA1=os.path.dirname(__file__)+'/test.json'

#-----------------------

sources= {
    'test':Source_Json(name='test',path=DATA1)
}

#-------------------
column_mapper= {
    
    0:'timestamp',
    1: 'open',
    2: 'high',
    3: 'low',
    4: 'close',
    5: 'volume',
    6: 'not-applicable'
}

def processor(col, schema):
    details= schema[col.name]
    return col.apply(details[0], **(details[1] if details[1:] else {}))

def process_nothing(col):
    return col

process_dict= {
    'timestamp': [pandas.Timestamp],
    'open': [process_nothing], #already float / integers and no nan values
    'high': [process_nothing], #already float / integers and no nan values
    'low':  [process_nothing], #already float / integers and no nan values
    'close': [process_nothing],  #already float / integers and no nan values 
    'volume': [process_nothing], #already float / integers and no nan values
    'not-applicable': [process_nothing], #already float / integers and no nan values
}

def clean_preprocessing(df,process_dict=process_dict,**kwargs):
    df = df.rename(columns=column_mapper)
    df=df.apply(processor, **{'schema':process_dict})
    return df
