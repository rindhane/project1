# Project Stock Analysis. 
This repository helps to build your own local setup to do the analysis of the stocks listed on the BSE. 

> Check out the analysis done on the index derivatives listed on the bombay stock exchange. [Link](https://www.google.com)  


***

**Commands**

#### To generat the local database

In the terminal, 
'''
git clone https://github.com/rindhane/stock_options
cd stock_options 
'''
then run 
'''python 
python file_downloader.py
'''
> Let it run for some_time and it will create a sqlite database with the name "equity_db.db" in the same folder with all the historical records.


#### To get a complete historical data of the stock in a dataframe. 

Execute this command within your program or jupyter notebook
df=data_to_pandas(scrip_no)

example show as following for hdfc bank stocks >>

'''python
from start_db import data_to_pandas
df=data_to_pandas(500180) #hdfc bank scrip code on bse is 500180
'''

##### Pending points 
To write the function to run live check of the database and the remaining data which have to be scraped again into the database based on the current date.