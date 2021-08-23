import unittest
import sqlite3
import os
from utilities.data_analysis import (Data,Source_sqlite,Source_Json)
import pandas as pd
import numpy as np

COLUMNS_DICT= {
    'DATE': [pd.Timestamp],
    'OPEN': [lambda x: float(x)], #already float / integers and no nan values
    'HIGH': [lambda x: float(x)], #already float / integers and no nan values
    'LOW':  [lambda x: float(x)], #already float / integers and no nan values
    'CLOSE': [lambda x: float(x)],  #already float / integers and no nan values 
    'LAST': [lambda x: float(x)], #already float / integers and no nan values
    'PREVCLOSE': [lambda x: float(x)], #already float / integers and no nan values
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
    df=pd.DataFrame(result,columns=cols,copy=True)
    if sorter is not None:
        df=df.sort_values(by=sorter)
    df=df.reset_index(drop=True)
    return df

def pre_processing(df,process_dict=COLUMNS_DICT,**kwargs):
    df=df.apply(processor, **{'schema':process_dict})
    return df

class test_stocksDataConnector(unittest.TestCase):
    def setUp(self):
        self.DATE_COLUMN='DATE'
        self.DATE_PROCESSOR=pd.Timestamp
        self.stock='BSE'+'500112'
        self.processedPath=os.path.dirname(
                    os.path.abspath(__file__))+'/processedDB.csv'
        self.processing=[('clean',cleaner),
                        ('preprocess',pre_processing)]
        self.raw=[('raw',None)]
        self.tablePath=os.path.dirname(
                    os.path.abspath(__file__))+'/tables.json'
        self.path=os.path.dirname(os.path.abspath(__file__))+'/test.db'
        self.db=sqlite3.connect(self.path)
        self.rawData=self.db.execute('select * from {table};'.format(table=self.stock)).fetchall()
        self.data=Data(stocks=Source_sqlite(path=self.path))
        self.tables=Data(tables=Source_Json(path=self.tablePath))
    def test_stock(self):
        test=self.data.action(self.stock, read=self.raw)
        check=pd.DataFrame(self.rawData)
        compare_result=0
        self.assertEqual(
            len(check.compare(test)),
            compare_result,
            'same raw data should be extracted')
        self.assertEqual(len(test), 3606)
    def test_stock_processed(self):
        test=self.data.action(self.stock,
                            read=self.processing,
                            size=3606,
                            )
        check=pd.read_csv(self.processedPath)
        check[self.DATE_COLUMN]=check[self.DATE_COLUMN].apply(self.DATE_PROCESSOR)
        self.assertIsInstance(test,pd.core.frame.DataFrame)
        self.assertEqual(len(check.compare(test)),0,'check processing function')
    def test_loader(self):
        test=self.tables.action(key=None,
                                read=self.raw,
                                loader=pd.DataFrame,
                                )
        self.assertIsInstance(test,pd.core.frame.DataFrame)
        self.assertEqual(len(test),10047,'check loader passing function test')
    def tearDown(self):
        self.db.close()
        del self.raw
        del self.data
        del self.db

if __name__=="__main__":
    unittest.main()