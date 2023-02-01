

from bs4 import BeautifulSoup
import requests,json
import sqlite3,time,traceback
from os import path
from datetime import datetime,timedelta
#pip install python-dateutil
from dateutil import parser



file_path = path.abspath(__file__) # full path of your script
dir_path = path.dirname(file_path) # full path of the directory of your script
DB_PATH = path.join(dir_path,'db_tradera.db') 
LIST_PATH = path.join(dir_path,'list_searches.txt') 



#DB COnnection and cursor
try:
	connection = sqlite3.connect(DB_PATH)
	cursor = connection.cursor()
except:
	print("CONNECTION TO DATABASE FAILED")
    
    
    

res = cursor.execute(f"SELECT Id,EndDate FROM tradera_data;")
res = res.fetchall()
format = "%Y-%m-%dT%H:%M:%S"

for entry in res:
    temp = entry[1].split(".")
    date_object = datetime.strptime(temp[0], format)
    delta = date_object -datetime.utcnow() 
    if delta < timedelta(days=-1):
        print(delta)
        res = cursor.execute(f"DELETE FROM tradera_data WHERE Id={entry[0]}; ")
        

#print(datetime.now(timezone.utc))
    
    
connection.commit()
connection.close()
