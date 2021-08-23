import sqlite3 as sqlite
from utilities.general.class_builders import self_setup_class
from google.cloud.sql.connector import connector
import os 

class BSEstockEntry(self_setup_class):
    security_TABLE='SC_CODE'
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.set_table()
    def set_table(self):
        setattr(self,'TABLE',self.get(self.__class__.security_TABLE))
    @classmethod
    def get_indicator_keys(cls,o=None):
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
        if o=='join':
            return ' , '.join(keys)
        if o=='create':
            return ' , '.join(keys)
        return keys
    def get_indicator_vals(self):
        keys=self.get_indicator_keys()
        result=list()
        for key in keys:
            result.append(self.transformer(key))
        return result
    @classmethod
    def get_information_keys(cls):
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
    @classmethod
    def get_execution_insertScript(cls,df,**kwargs):
        script = ''
        i=0
        for row in df.iloc:
            stock=cls(**row)
            values=stock.get_indicator_vals_string()
            statement=f" Insert INTO {stock['TABLE']} VALUES ({values}) ; "
            script = script + statement
        return script
    @classmethod
    def get_execution_insert(cls,row,**kwargs):
        stock=cls(**row)
        values=stock.get_indicator_vals_string()
        statement=f" Insert INTO {stock['TABLE']} VALUES ({values}) ; "
        return statement

class BSE_DB(self_setup_class):
    #universal constants for BSE_DB
    DATE_TABLE='DATE_RECORD'
    DATE_HEADS= dict(DATE = 'varchar' , STATUS = 'integer')
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
    def create_date_table(self,**kwargs):
        heads=', '.join(self.__class__.DATE_HEADS)
        return self.create_table(self.__class__.DATE_TABLE,
                                 heads,
                                ) 
    def isDate(self,date):
        date=str(date)
        cursor=self.initiate_connection()
        result=cursor.execute(
            f"select * from  {self.__class__.DATE_TABLE}" 
            ).fetchall()
        dates=set(vals[0] for vals in result)
        return date in dates
    def insert_date(self,date,status):
        date=str(date)
        date="'"+date+"'"
        heads=', '.join(self.__class__.DATE_HEADS)
        return self.insert_row(
                        self.__class__.DATE_TABLE,
                        heads,
                        f'{date} , {status}')
    def create_info_table(self):
        self.INFO_TABLE='INFO_TABLE'
        keys=BSEstockEntry().get_information_keys()
        heads=" , ".join(keys)
        self.create_table(self.INFO_TABLE , heads)
        return True
    def execute_script(self,script):
        self.get_cursor().executescript(script)
        self.commit()
        return True

class BSEstockEntryNew(BSEstockEntry):
    '''
    Usage:
        1. Create new table object :
            table=TABLE(field1=type1,field2=type2,....)
            eg: customers=TABLE(name='varchar, age='integer')
        2. get table_string for
    Description:
        Helper class to create statements from its model to be provided as sql statement 
    '''
    types=dict(
            default='varchar',
            varchar= 'varchar(255)',
            integer='int',)
    @classmethod
    def string_creator(cls,keys):
        result=''
        separator=' '
        end=len(keys)-1
        for i,key in enumerate(keys):
            kind=cls.kind_string(
                getattr(cls,key,cls.types['default'])
                )
            tmp=separator +\
                str(key) +\
                separator +\
                kind+ (',' if i<end else separator)
            result=result+tmp
        return result
    @classmethod
    def get_indicator_keys(cls,o=None):
        keys={
             'DATE':'varchar', 
             'OPEN':'varchar', 
             'HIGH':'varchar',
             'LOW':'varchar', 
             'CLOSE':'varchar', 
             'LAST':'varchar',
             'PREVCLOSE':'varchar',
             'NO_TRADES':'varchar',
             'NO_OF_SHRS':'varchar',
             'NET_TURNOV':'varchar',
             'TDCLOINDI':'varchar',
            }
        if o is None:
            return list(keys.keys())
        if o=='join':
            return ' , '.join(list(keys.keys()))
        if o=='create':
            return cls.string_creator(keys)
    @classmethod
    def kind_string(cls,kind):
        return cls.types.get(kind,cls.types[cls.types['default']])

class BSE_DB_cloud(BSE_DB):
    '''
    Description:
        Class to act as single point to access the database.
        This class primarily handles the sql database of the gcloud sql. 
    USAGE: 
        1. Create new database connector: 
        stock=BSE_DB_cloud (
            db_path=path_to_cloud_service_account,
            project=project_id,
            region=instance_ragion,
            instance=instance_name,
            user=user_name # generally it is root,
            password=password,
            db=database_name,
        )
    '''
    default_database_driver='pymysql'
    def get_db_path(self):
        return self.get('db_path','secrets/auth.json')
    def build_cred(self,*a,**kw):
        project=getattr(self,'project')
        region=getattr(self,'region')
        instance=getattr(self,'instance')
        user=getattr(self,'user')
        password=getattr(self,'password')
        db=getattr(self,'db_name')
        driver=self.__class__.default_database_driver
        args=[f'{project}:{region}:{instance}',f'{driver}']
        kwargs=dict(user=user,password=password,db=db)
        return args,kwargs
    def initiate_connection(self):
        if self.get('connection'):
            return self.get('connection').cursor()
        os.environ['GOOGLE_APPLICATION_CREDENTIALS']=self.get_db_path()
        args,kwargs=self.build_cred()
        conn=connector.connect(*args,**kwargs)
        setattr(self,'connection',conn)
        return conn.cursor()
    def get_tables(self):
        cursor=self.initiate_connection()
        cursor.execute(
            "SHOW TABLES;"
            )
        result=cursor.fetchall()
        tables=set(vals[0] for vals in result)
        cursor.close()
        return tables
    def execute_script(self,statement):
        self.get_cursor().execute(statement)
        self.commit()
        return True
    def create_date_table(self,**kwargs):
        cls=kwargs.get('cls',BSEstockEntryNew)
        heads=cls.string_creator(self.__class__.DATE_HEADS)
        return self.create_table(self.__class__.DATE_TABLE,
                                 heads,
                                )
    def isDate(self,date):
        date=str(date)
        cursor=self.initiate_connection()
        cursor.execute(
            f"select * from  {self.__class__.DATE_TABLE}" 
            )
        result=cursor.fetchall()
        dates=set(vals[0] for vals in result)
        return date in dates
    