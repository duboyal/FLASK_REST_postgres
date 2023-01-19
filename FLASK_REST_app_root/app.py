from flask import Flask, redirect
from flask import request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import uuid
import json
import hashlib
from db import stores, items
from flask_smorest import abort
import os


# -------- THIS IS TO WORK WITH JSON ------------

#once database is conected just get rid 
# Opening JSON file

def appendJSON(file_path, my_dict, stores_str, my_id):

    if os.stat(file_path).st_size == 0:
        data = {stores_str: {my_id : {my_dict}}} #this sttructure is wrong ok ok 

    else:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)


            if isinstance(data[stores_str], dict):
                data[stores_str][my_id] = my_dict


    with open(file_path, "w") as json_file:
        json.dump(data, json_file)





# --------- this is to set up databases

app = Flask(__name__) #basically boiler plate our instance of flask


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ifxlhppb:Uclz9zMErLRf1s1azg1rVe8LyyhRn8nB@batyr.db.elephantsql.com/ifxlhppb"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
# ^^ok those need to be set before defining db
db = SQLAlchemy(app) # igues this is here and then  gets imported. but is that design?





# ------- ROUTES SECTION 

@app.route("/")
def hello():
    return redirect("http://127.0.0.1:5000/store") #need to make this more dynamic like get the host get the port then put an endpoint

@app.get("/store") #http://127.0.0.1:5000/store
def get_stores():
    return {"stores":stores}

@app.get("/item") #http://127.0.0.1:5000/store
def get_items():
    return {"items":list(items.values())} #dictionary formate



# need error haandling 
#we expect 
@app.post("/store") #http://127.0.0.1:5000/store
def create_store():
    store_data = request.get_json() # we expect price of item to be there, store id, and name)
    # -----------------------------
    #           ERROR HANDLING CHUNK
    # we expect price of item to be there, store id, and name)
    if (
        "name" not in store_data or "items" not in store_data #or "name" not in store_data #add marshmellow for typing
    ):
        # return abort(404, message="bad request, we need price, store id and name in json payload to creaate")
        return {"message" : "bad request, we need items and name in json payload to creaate store"}, 404
    
    with open("stores.json", "r") as json_f:
        stores = json.load(json_f)

    # for store in stores.values():
    #     if (
    #         store_data["name"] == store["name"] and store_data["items"] == store["store_id"]
    #     ):
    #         return {"message" : "Store already exists"}, 404
    # ---------------

    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id} #unpacking the json and also adding the new wdict item for store_id
    
    print(stores)
    stores[store_id] = new_store
    #stores["stores"][store_id] = new_store


    appendJSON('stores.json',new_store,"stores", store_id)

    return  new_store,201


@app.post("/item")
def create_item():

    item_data = request.get_json() #used to be request_data
    # -----------------------------
    #           ERROR HANDLING CHUNK
    # we expect price of item to be there, store id, and name)
    if (
        "price" not in item_data or "store_id" not in item_data or "name" not in item_data #add marshmellow for typing
    ):
        # return abort(404, message="bad request, we need price, store id and name in json payload to creaate")
        return {"message" : "bad request, we need price, store id and name in json payload to creaate"}, 404

    for item in items.values():
        if (
            item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]
        ):
            return {"message" : "item already exists"}, 404


    if item_data["store_id"] not in stores:
        # return abort(404, message="store not dfound")
        return {"message" : "Store Not Found"}, 404
    # ---------------


    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    appendJSON('items.json',item)
    return item, 201


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        with open('stores.json') as f:
            # jstr = f.read()
            stores = json.load(f)
            print("hey")
            print(stores)
        #structure should be store["stores"][id] = {name, blah}

            try:

                return stores['stores'][store_id]
            except Exception as error:
                return {"message" : "store not found"}, 404

            #     with open(file_path, "r") as json_file:
            # data = json.load(json_file)
    except KeyError:
        return {"message" : "store not found"}, 404



@app.get("/item/<string:item_id>") #http://127.0.0.1:5000/store
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "item not found"}, 404








# from models import ItemModel, StoreModel

# current_date = datetime.today().date()

# new_item = ItemModel( name = "TEST  item", price = 50) 

# new_store = StoreModel(name = "TEST  store", items = [new_item] )

# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     db.session.add(new_store) #basically i can probably just get rid of this line 
#     db.session.commit()

# # post method to add a store
# # @app.post("/store") #http://127.0.0.1:5000/store
# # def add_stores():
# #     return {"stores":stores}

'''
export FLASK_APP=__init__ 
export FLASK_APP=app
flask run
'''