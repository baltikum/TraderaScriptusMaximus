from bs4 import BeautifulSoup
import requests,json
import sqlite3,time,traceback
from os import path
from datetime import datetime

file_path = path.abspath(__file__) # full path of your script
dir_path = path.dirname(file_path) # full path of the directory of your script
LIST_PATH = path.join(dir_path,'list_searches_2.txt') 


#Get searches fom file
list_of_searches = []
with open(LIST_PATH, "r" ) as searchList :
    while True:
        line = searchList.readline()
        if len(line) != 0:
            list_of_searches.append(line)
            time.sleep(0.01)
        else:
            break

for entry in list_of_searches:
    test = entry.split("https://www.tradera.com/search?q=")
    print(test[1])