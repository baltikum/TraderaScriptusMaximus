from flask import Flask,render_template,make_response,request,send_from_directory
import sqlite3, json
from os import path
import os

file_path = path.abspath(__file__) # full path of your script
dir_path = path.dirname(file_path) # full path of the directory of your script
DB_PATH = path.join(dir_path,'db_tradera.db') 
#print(DB_PATH)


app = Flask(__name__)

standard_item = [
                "itemId",
                "price",
                "shortDescription",
                "imageUrl",
                "itemUrl",
                "itemType",
                "totalBids",
                "endDate",
                "startDate",
                "isActive",
                "sellerAlias",
                "showItem",
                "BidOnItem",
                "ObservedItem"
                ]

def get_full_search_data():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    result = cursor.execute("""SELECT * FROM tradera_data  WHERE ShowItem = 1 ; """)
    all_results = result.fetchall()

    print(all_results)

    json_list = []
    for entry in all_results:
        item_dictionary = {}
        for i,entry_data in enumerate(entry):
            item_dictionary[standard_item[i]] = str(entry_data)
        
        json_list.append(item_dictionary)
    connection.close()
    return json_list

def get_one_search(id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    try:
        int(id)
    except:
        return 
        
    result = cursor.execute(f"""SELECT * FROM tradera_data WHERE id = {id} ;""")
    result = result.fetchone()
    connection.close()
    item_dict = {}
    for i,entry_data in enumerate(result):
            item_dict[standard_item[i]] = str(entry_data)
    return item_dict




@app.route('/', methods = ['GET'])
def get_webpage():
    response = make_response(render_template('index.html',points=("{\"objectList\" : " + json.dumps(get_full_search_data(),indent=3) + "}")))
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

@app.route('/return_search_data', methods = ['GET'])
def return_search_data():
    temp = get_full_search_data()
    response = make_response("{\"objectList\" : " + json.dumps(temp,indent=3) + "}")
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response
    
@app.route('/fetch_id/<id>', methods = ['GET'])
def fetch_id(id):
    try:
        int(id)
    except:
        return 
    temp = get_one_search(id)
    response = make_response("{\"object\" : " + json.dumps(temp,indent=3) + "}")
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response
    
@app.route('/hide_id/<id>', methods = ['POST'])
def hide_item_on_id(id):
    intId = 0
    try:
        intId = int(id)
    except:
        return 
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = f"UPDATE tradera_data SET ShowItem = 0 WHERE Id = {intId};"
    result = cursor.execute(query)
    connection.commit()
    connection.close()
    return {"result": "True"}

@app.route('/show_id/<id>', methods = ['POST'])
def show_item_on_id(id):
    intId = 0
    try:
        intId = int(id)
    except:
        return 
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = f"UPDATE tradera_data SET ShowItem = 1 WHERE Id = {intId};"
    result = cursor.execute(query)
    connection.commit()
    connection.close()
    return {"result": "True"}

@app.route('/observed_id/<id>', methods = ['POST'])
def observed_id(id):
    intId = 0
    try:
        intId = int(id)
    except:
        return 
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    result = cursor.execute(f"UPDATE tradera_data SET ObservedItem = 1 WHERE Id = {intId};")
    connection.commit()
    connection.close()
    return {"result": "True"}

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'),'favicon.ico')

if __name__=='__main__':
    app.run(host='0.0.0.0')
