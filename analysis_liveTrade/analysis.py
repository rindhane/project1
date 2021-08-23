import pandas as pd
from utilities.general.time_helpers import (
                                            set_timezone,
                                            get_range_slots,
                                            )
from utilities.data_analysis import (
                                    Data, 
                                    Source, )

from .data_definition import ( sources,
                              clean_preprocessing,
                            )
import datetime
#----------------------------------------
#constants
date_focus='2021-04-22'
tz=datetime.timezone(datetime.timedelta(hours=5,minutes=30))


#-----------------------------
#analysis scripts
data=Data(**sources)
df=pd.read_json(data.get('test').reader())    
df = clean_preprocessing(df)
df=df.set_index('timestamp')
start, end=next(get_range_slots(date_focus,tz=True))
df_range=df[start:end]
print(df_range)
t1=datetime.datetime.combine(start,datetime.time(hour=10,minute=0,second=0))
t1=t1.replace(tzinfo=tz)
t2=t1+datetime.timedelta(hours=1,minutes=0,seconds=0)
dat=df_range[t1:t2]
