import datetime

class self_setup_class : 
    '''helper class to setup class which can create attributes from 
    the passed key value pairs during initalization of instance'''
    def __init__(self,**kwargs):
        self.set_inputs(**kwargs)
    def set_inputs(self,**inputs):
        for key in inputs:
            setattr(self,key,inputs.get(key))
    def __getitem__(self,tag):
        if not isinstance(tag,str):
            raise ValueError (f"{tag} is not string , provide key in string format" )
        return getattr(self,tag,None)
    def __setitem__(self,tag,value):
        if not isinstance(tag,str):
            raise ValueError (f"{tag} is not string , provide key in string format" )
        setattr(self,tag,value)
        return value
    def keys(self):
        return list(vars(self).keys())
    def items(self):
        return list(vars(self).items())
    def get(self,key,default=None):
        if self.__getitem__(key) is None :
            return default
        return self.__getitem__(key)

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
    def read_all(self,key,**kwargs):
        return self.get(key).read_all(**kwargs)
    def clean(self,func,**kwargs):
        pass
    def processing(self,func,**kwargs):
        pass

class Source(self_setup_class):
    def reader(self,**kwargs):
        return open(getattr(self,'path',None),'r')
    def read_all(self,**kwargs):
        return self.reader().read()

def set_timezone(date,**kwargs):
    #setting time at midnight start of the day i.e 00:00 hrs
    date=datetime.datetime.combine(date,datetime.time(0,0))
    tz=datetime.timezone(datetime.timedelta(hours=5,minutes=30))
    if kwargs.get('tz_choice',None) =='in':
        tz=pytz.timezone(pytz.country_timezones('in')[0])
        return tz.localize(date)
    return date.replace(tzinfo=tz)    

def get_date_range(initial,end=None,**kwargs):
    #initial date should be in iso format.
    #write a check for conformance of string to iso-format
    start=datetime.date.fromisoformat(initial)
    if end :
        end=datetime.date.fromisoformat(end)
        return start,end
    return start, start+datetime.timedelta(days=kwargs.get('gap',1))

def get_range_slots(initial,gap=1,n_period=1,**kwargs):
    for i in range(0,n_period):
        start , end= get_date_range(initial,gap=gap,)
        if kwargs.get('tz',None):
            yield set_timezone(start,**kwargs),set_timezone(end,**kwargs) 
        else:
            yield start,end 
        initial=end.isoformat() 
