

from bs4 import BeautifulSoup
import requests,json
import sqlite3

#DB COnnection and cursor
connection = sqlite3.connect("db_tradera_searches.db")
cursor = connection.cursor()



#Get searches fom file
list_of_searches = []
with open("list_searches.txt", "r" ) as searchList :
    while True:
        line = searchList.readline()
        if len(line) != 1:
            list_of_searches.append(line)
        else:
            break



"""
cursor.execute("DROP TABLE saved_searches")
connection.commit()"""


cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_searches (
        Id INTEGER NOT NULL,
        Search TEXT,
        SearchUrl TEXT
    )""")
