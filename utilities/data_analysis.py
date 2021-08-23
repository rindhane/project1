from utilities.general.class_builders import self_setup_class
import sqlite3
import pandas as pd
import json

class Data (self_setup_class ):
    """
    It is the model that represents the whole data
    Key constitutents:
        Tables:
            1.self[key] is the method to access the table source from self (Data instance)
            2.all keys in vars(self) are pointers Source object
        Sources:
            1.These pointers to original source of data
            2.These are accessed through the output of the self.get(key).read_all(*kwargs)
                Note: key is of required table 
    """
    def action(self,key,loader=True,**kwargs):
        actions=kwargs.get('read', None)
        if actions is not None:
            if loader is True:
                return self.data_loader(self.read_all(key=key,actions=actions,**kwargs),**kwargs)
            if loader is False:
                return self.read_all(key=key,actions=actions,**kwargs)
            if callable(loader):
                return loader(self.read_all(key=key,actions=actions,**kwargs))
            else:
                raise ValueError(f"{loader} object must be callable or bool value")
    def read_all(self,key,**kwargs):
        sources_dict=vars(self)
        for name in sources_dict:
            #need to improve to handle yielding the various sources
            #yield from self.read_source(key,name,**kwargs)
            yield from self.read_source(key,name,**kwargs)
    def read_source(self,key,name,**kwargs):
        for data in getattr(self,name).read_all(key=key, **kwargs):
            yield self.process_data(data,**kwargs)
    def process_data(self,data,actions=None,**kwargs):
        if self.check_actions(actions):
            for action in actions:
                label,processor=action
                if label=='raw':
                    return data
                #completer processing of given data in one go into memory space
                data=self.processEngine(processor=processor, data=data)
            return data
        return None
    def processEngine(self,processor,**kwargs):
        return processor(kwargs.get('data'))
    def check_actions(self,actions):
        if not isinstance(actions,list):
            raise TypeError('read input must be a list')
        for action in actions:
            if not isinstance(action,(list,tuple)):
                raise TypeError(f'{action} is not a type of list or tuple')
            if len(action)!=2:
                raise ValueError(f'{action} should contain only 2 parameters but\
                {len(action)} parameters were given')
        return True
    def data_loader(self, iterator,**kwargs):
        return pd.concat(
                    (pd.DataFrame(i) for i in iterator),
                            ignore_index=True)

class Source(self_setup_class):
    def reader(self,**kwargs):
        pass
    def read_all(self,**kwargs):
        pass
    def close(self,**kwargs):
        pass
    def dispatcher(self,**kwargs):
        pass

class Source_Json(Source):
    def reader(self,**kwargs):
        if self.get('connection',None):
            return self.connection
        self.connection=open(getattr(self,'path',None),'r')
        return self.reader(**kwargs)
    def read_all(self,**kwargs):
        data=json.loads(self.reader().read())
        self.close()
        return data
    def close(self,**kwargs):
        self.connection.close()
        del self.connection
        return True

class Source_sqlite(Source):
    read_size=500
    def reader(self,**kwargs):
        if self.get('connection',None):
            return self.connection
        self.connection=sqlite3.connect(getattr(self,'path',None))
        return self.reader(**kwargs)
    def read_all(self,**kwargs):
        table=kwargs.get('key',None)
        conn=self.reader(**kwargs).cursor()
        conn.execute('select * from {table}'.format(table=table))
        results=conn.fetchall()
        size=kwargs.get('size',self.__class__.read_size)
        return self.dispatcher(results,size=size)
    def close(self,**kwargs):
        self.connection.close()
        del self.connection
        return True
    def dispatcher(self,results,**kwargs):
        size=kwargs.get('size')
        tmp=iter(results)
        check=True
        while check :
            slot=[]
            for i in range(0,size):
                try:
                    slot.append(next(tmp))
                except StopIteration:
                    check=False
                    break
            yield slot


