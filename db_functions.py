import sqlite3
from helper_file import convert_keys_to_string, convert_keys_to_string_key

def create_table(table_name,connection):
    var=str(table_name)
    connection.execute (''' CREATE TABLE  {0}
                   (DATE varchar(10),
                    OPEN real ,
                    HIGH real, 
                    LOW real, 
                    CLOSE real,  
                    LAST real, 
                    PREVCLOSE real,  
                    NO_TRADES integer, 
                    NO_OF_SHRS integer,  
                    NET_TURNOV integer, 
                    TDCLOINDI text)'''.format(var))   
    return True


class table_structure(object):
    @staticmethod
    def var():
        real="real"
        integer="integer"
        return real, integer
    
    def __init__(self,**kwargs): 
        real, integer=self.var()    
        self.dict = {"DATE": "varchar(10)",
             "OPEN" : real ,
             "HIGH" : real,
             "LOW": real, 
             "CLOSE": real,  
             "LAST": real, 
             "PREVCLOSE": real,  
             "NO_TRADES": integer, 
             "NO_OF_SHRS": integer,  
             "NET_TURNOV": integer, 
             "TDCLOINDI": "text"} 

#function is working of . need to check it's working against create_table function
#presently not being used
def create_table_2(table_name,curr):
    bse=table_structure() # using class structure to create table scheme
    temp1=list(bse.dict.keys())
    final_temp=list()
    for item in bse.dict.keys():
        temp1.append(bse.dict[item])
    for i in range (0,len(bse.dict)):
        final_temp.append(temp1[i])
        final_temp.append(temp1[len(bse.dict)+i])
    s=""
    for items in zip(temp1[0:len(bse.dict)],temp1[len(bse.dict):]):
        s=s+" ".join(items)
        s=s+" "+","  
    s=s[:len(s)-1]
    curr.execute("CREATE TABLE {0}".format(table_name)+"("+s+")")
    return True





def insert_row(var_table, dict_row , cursor): 
    column_string=convert_keys_to_string(dict_row.keys()) # column_string
    pholder=convert_keys_to_string_key(dict_row.keys()) # column_string_key-placeholder
    #checking for table and writing into the table : 
    try : 
        cursor.execute( f'''INSERT INTO {var_table}  {column_string} VALUES {pholder} ''', dict_row )
    except sqlite3.OperationalError :
        create_table(var_table,cursor)
        cursor.execute( f'''INSERT INTO {var_table}  {column_string} VALUES {pholder} ''', dict_row )
    return True


def create_main_index_table(connection):
    var="main_index_table"
    connection.execute (''' CREATE TABLE  {0}
                   (exchange text,
                    security_code varchar(16) ,
                    security_name text, 
                    early varchar(10),  
                    recent varchar(10),
                    group varchar(5), 
                    security_type text)'''.format(var))   
    return True


def get_date_table_name():
    date_table="date_record"
    return date_table

def create_date_table(connection):
    date_table=get_date_table_name()
    connection.execute(f''' create table {date_table} (
                            date varchar(10),
                            status varchar(10)
                          )
                        ''')

def update_date_record(cursor,date_value,status_code):
    date_table=get_date_table_name()
    try :
        cursor.execute(f''' insert into {date_table} (date, status) values (?,?)  
                        ''', (date_value, status_code) )
    except sqlite3.OperationalError :
        create_date_table(cursor)
        cursor.execute(f''' insert into {date_table} (date, status) values (?,?)  
                        ''',(date_value,status_code) )
    return True

