
from bs4 import BeautifulSoup
import requests,json
import sqlite3,time,traceback
from os import path
from datetime import datetime

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


#delete table
"""cursor.execute("DROP TABLE tradera_data;")
connection.commit()"""

#Check if and create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tradera_data (
        Id INTEGER primary key, 
        Price INTEGER,
        ShortDescription TEXT,
        ImageUrl TEXT,
        ItemUrl TEXT,
        ItemType TEXT,
        TotalBids INTEGER,
        EndDate TEXT,
        StartDate TEXT,
        IsActive TEXT,
        SellerAlias TEXT,
        ShowItem INTEGER, 
        BidOnItem INTEGER,
        ObservedItem INTEGER 
    );""")

#Fetches and returns Boolean return and json string result or empty string if fail.
def get_saved_search(link):

    r = requests.get(link)

    if str(r) != '<Response [200]>':
        res = False
        return res, ''
        
    s = BeautifulSoup(r.content, features="lxml")
    data = s.find(id='init-data')
    temp = str(data)
    temp = temp.split('\'')
    data = json.loads(temp[1])
    res = True
    return res, json.dumps(data['discoverResponse'], indent=4)

#Check if item exists in DB
def check_if_available_in_database(id):
    intId = int(id)
    res = cursor.execute(f"SELECT * FROM tradera_data WHERE Id = {intId} ;")
    exists = res.fetchone()
    return True if exists else False


for entry in list_of_searches:

    res, data = get_saved_search(entry)

    if res:
        items = json.loads(data)['items']

        for item in items:
            item['startDate'] = datetime.now().isoformat()
            

            try:
                if not check_if_available_in_database(item['itemId']):
                    #ADD
                    description = str(item['shortDescription'])
                    shortDescription = "".join(character for character in description if character not in "'")
                    queryString = (
                        "INSERT INTO tradera_data VALUES (" +
                            f"{item['itemId']}," +
                            f"{item['price']}," +
                            f"'{shortDescription}'," +
                            f"'{item['imageUrl']}'," +
                            f"'{item['itemUrl']}'," +
                            f"'{item['itemType']}'," +
                            f"{item['totalBids']}," +
                            f"'{item['endDate']}'," +
                            f"'{item['startDate']}'," +
                            f"'{item['isActive']}'," +
                            f"'{item['sellerAlias']}',1,0,0)"
                    )
                    
                else:
                    
                    queryString = (
                            "UPDATE tradera_data SET " +
                                f"Price = {item['price']}," +
                                f"TotalBids = {item['totalBids']}, " +
                                f"EndDate = '{item['endDate']}'" +
                                f"WHERE Id = {item['itemId']}" 
                    )
            

                print(queryString)
                res = cursor.execute(queryString)
            except sqlite3.OperationalError:
                print(f"OPERATIONAL ERROR ON {queryString}")
                traceback.print_exc()


connection.commit()
connection.close()

            
