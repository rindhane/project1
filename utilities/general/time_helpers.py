import datetime as dt
#import pytz

def set_timezone(date,**kwargs):
    #setting time at midnight start of the day i.e 00:00 hrs
    date=dt.datetime.combine(date,dt.time(0,0))
    tz=dt.timezone(dt.timedelta(hours=5,minutes=30))
    if kwargs.get('tz_choice',None) =='in':
        tz=pytz.timezone(pytz.country_timezones('in')[0])
        return tz.localize(date)
    return date.replace(tzinfo=tz)    

def date_date_range_ends(initial,end=None,**kwargs):
    #initial date should be in iso format.
    #write a check for conformance of string to iso-format
    start=dt.date.fromisoformat(initial)
    if end :
        end=dt.date.fromisoformat(end)
        return start,end
    return start, start+dt.timedelta(days=kwargs.get('gap',1))

def get_range_slots(initial,gap=1,n_period=1,**kwargs):
    for i in range(0,n_period):
        start , end= date_date_range_ends(initial,gap=gap,)
        if kwargs.get('tz',None):
            yield set_timezone(start,**kwargs),set_timezone(end,**kwargs) 
        else:
            yield start,end 
        initial=end.isoformat() 

def date_range_generator(date_start, date_end):
    #dates expected in isoformat
    start =  dt.date.fromisoformat(date_start)
    end = dt.date.fromisoformat(date_end)
    span = (end-start).days
    for i in range(0,span,(1 if span>0 else -1)):
        date=start+dt.timedelta(days=i)
        yield date

