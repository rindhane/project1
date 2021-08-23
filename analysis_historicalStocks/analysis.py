from utilities.data_analysis import Data
from .data_definition import (sources, 
                            cleaner,
                            pre_processing,
                            keys)
import pandas as pd

data=Data(**sources)
result1=data.action('BSE500112',read=[
                                ('clean',cleaner),
                                ('preprocess',pre_processing)],
                              size=14000)

codes=Data(**keys)
result2=codes.action(key='any',read=[('raw',None)],
                    loader=pd.DataFrame)