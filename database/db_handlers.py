import sqlite3 as sqlite
from .helper_file import self_setup_class

class BSEstockEntry(self_setup_class):
    security_TABLE='SC_CODE'
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.set_table()
    def set_table(self):
        setattr(self,'TABLE',self.get(BSEstockEntry.security_TABLE))
    def get_indicator_keys(self):
        keys=[
             'DATE', 
             'OPEN', 
             'HIGH',
             'LOW', 
             'CLOSE', 
             'LAST',
             'PREVCLOSE',
             'NO_TRADES',
             'NO_OF_SHRS',
             'NET_TURNOV',
             'TDCLOINDI',
             ]
        return keys
    def get_indicator_vals(self):
        keys=self.get_indicator_keys()
        result=list()
        for key in keys:
            result.append(self.transformer(key))
        return result
    def get_information_keys(self):
        keys=['SC_CODE', 'SC_NAME', 'SC_GROUP', 'SC_TYPE']
        return keys
    def get_information_vals(self):
        keys=self.get_information_keys()
        result=list()
        for key in keys:
            result.append(self.transformer(key))
        return result
    def transformer(self,key,**kwargs):
        if key=='DATE':
            return self.get(key).isoformat()
        return str(self.get(key))
    def get_list_string(self,list_):
        result= ""
        last=len(list_)-1
        for idx,item in enumerate(list_):
            #adding string quotes to give string item
            item="'"+str(item)+"'"
            result=result+" "+item+ (" , " if idx<last else " ")
        return result
    def get_indicator_vals_string(self):
        list_=self.get_indicator_vals()
        return self.get_list_string(list_)
    def get_information_vals_string(self):
        list_=self.get_information_vals()
        return self.get_list_string(list_)

class BSE_DB(self_setup_class):
    #db_path defined during initialization
    def get_db_path(self):
        return self.get('db_path','equity_db.db')
    def initiate_connection(self):
        if self.get('connection'):
            return self.get('connection').cursor()
        conn=sqlite.connect(self.get_db_path())
        setattr(self,'connection',conn)
        return conn.cursor()
    def get_cursor(self):
        if self.get('cursor'):
            return self.cursor
        self.cursor=self.initiate_connection()
        return self.cursor
    def close_connection(self):
        self.get_cursor().close()
        delattr(self,'cursor')
        self.initiate_connection().close()
        delattr(self,'connection')
        return True
    def commit(self):
        self.connection.commit()
    def get_tables(self):
        cursor=self.initiate_connection()
        result=cursor.execute(
            "select * from sqlite_master where type='table'"
            ).fetchall()
        tables=set(vals[1] for vals in result)
        cursor.close()
        return tables
    def check_isTable(self,table_name):
        table=str(table_name)
        return table in self.get_tables()
    def tables_not_available(self,tables):
        result=list(set(tables).difference(self.get_tables()))
        return result
    def create_table(self,table_name,headers):
        cursor=self.get_cursor()
        cursor.execute("CREATE TABLE {table} ( {headers} )".
                        format( 
                            table=str(table_name),
                            headers=headers
                                )
                        )   
        self.commit()
        return True
    def insert_row(self, table, heads, values,):
        cursor=self.get_cursor()
        cursor.execute( f'''INSERT INTO {str(table)} ( {str(heads)} ) VALUES ( {str(values)} ) ''')
        self.commit()
        return True
    def create_date_table(self):
        TABLE='DATE_RECORD'
        self.DATE_TABLE=TABLE
        heads= " DATE , STATUS "
        self.DATE_HEADS=heads
        return self.create_table(TABLE,heads) 
    def isDate(self,date):
        date=str(date)
        cursor=self.initiate_connection()
        result=cursor.execute(
            f"select * from  {self.DATE_TABLE}" 
            ).fetchall()
        dates=set(vals[0] for vals in result)
        return date in dates
    def insert_date(self,date,status):
        date=str(date)
        date="'"+date+"'"
        return self.insert_row(
                        self.DATE_TABLE,
                        self.DATE_HEADS,
                        f'{date} , {status}')
    def create_info_table(self):
        self.INFO_TABLE='INFO_TABLE'
        keys=BSEstockEntry().get_information_keys()
        heads=" , ".join(keys)
        self.create_table(self.INFO_TABLE , heads)
        return True

