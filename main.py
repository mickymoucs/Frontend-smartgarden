from fastapi import FastAPI, HTTPException, Body
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv(".env")
username = os.getenv("username")
password = os.getenv("password")

client = MongoClient(
    f"mongodb://{username}:{password}@mongo.exceed19.online:8443/?authMechanism=DEFAULT"
)

db = client["exceed08"]
collection = db["my_little_garden"]

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Moisture(BaseModel):
    moisture_value: int


class Sprinkle(BaseModel):
    is_auto: bool
    is_active: bool


class BuzzerSunroof(BaseModel):
    buzzer: bool
    sunroof: bool

class Data(BaseModel):
    moist_value: int
    moist_default: int
    sprinkle_1: Sprinkle
    sprinkle_2: Sprinkle
    buzzer: bool
    sunroof: bool


def moisture_to_percentage(moisture):
    percentage = int((moisture/1023)*100)
    return percentage


def percentage_to_moisture(percentage):
    percentage = int((percentage/100)*1023)
    return percentage


@app.get("/")
def read_root():
    return {"Hello": "Welcome to my little garden."}


@app.get("/garden/all")
def read_all_garden():
    data = collection.find({}, {"_id": False})
    moist = data[0]
    sprink = data[1]
    buz_sun = data[2]
    for_send = {
        "moist_value": moisture_to_percentage(moist["moist_value"]),
        "moist_default": moisture_to_percentage(moist["moist_default"]),
        "sprinkle_1": {
            "is_auto": sprink["sprinkle_1"]["is_auto"],
            "is_activate": sprink["sprinkle_1"]["is_activate"]
        },
        "sprinkle_2": {
            "is_auto": sprink["sprinkle_2"]["is_auto"],
            "is_activate": sprink["sprinkle_2"]["is_activate"]
        },
        "buzzer": buz_sun["buzzer"],
        "sunroof": buz_sun["sunroof"]
    }
    return for_send


@app.post("/garden/update")
def update_garden(data: Data = Body()):
    result = list(collection.find({}, {"_id": False}))
    for i in result:
        if i["name"] == "sprinkle":
            is_auto_1 = collection.find_one({"name": "sprinkle"}, {"_id": False})["sprinkle_1"]["is_auto"]
            is_auto_2 = collection.find_one({"name": "sprinkle"}, {"_id": False})["sprinkle_2"]["is_auto"]
            is_active_1 = collection.find_one({"name": "sprinkle"}, {"_id": False})["sprinkle_1"]["is_activate"]
            is_active_2 = collection.find_one({"name": "sprinkle"}, {"_id": False})["sprinkle_2"]["is_activate"]
            if is_auto_1 == True and is_active_1 == True:
                collection.update_one({"name": "moisture"}, {"$set": {"moist_default": percentage_to_moisture((data.moist_default)), "moist_value": percentage_to_moisture((data.moist_value))}})
            elif is_auto_1 == False and is_active_1 == False:
                collection.update_one({"name": "moisture"}, {"$set": {"moist_default": percentage_to_moisture((data.moist_default)), "moist_value": percentage_to_moisture((data.moist_value))}})
            elif is_active_1 == True:
                collection.update_one({"name": "moisture"}, {"$set": {"moist_default":  percentage_to_moisture((data.moist_default)), "moist_value": percentage_to_moisture((data.moist_value))}})
            elif is_auto_2 == True and is_active_2 == True:
                collection.update_one({"name": "moisture"}, {"$set": {"moist_default": percentage_to_moisture((data.moist_default)), "moist_value": percentage_to_moisture((data.moist_value))}})
            elif is_auto_2 == False and is_active_2 == False:
                collection.update_one({"name": "moisture"}, {"$set": {"moist_default": percentage_to_moisture((data.moist_default)), "moist_value": percentage_to_moisture((data.moist_value))}})
            elif is_active_2 == True:
                collection.update_one({"name": "moisture"}, {"$set": {"moist_default":  percentage_to_moisture((data.moist_default)), "moist_value": percentage_to_moisture((data.moist_value))}})

        if i["name"] == "moisture":
            moisture = i["moist_value"]
            moisture_default = i["moist_default"]
            is_auto_1 = collection.find_one({"name": "sprinkle"}, {"_id": False})["sprinkle_1"]["is_auto"]
            is_auto_2 = collection.find_one({"name": "sprinkle"}, {"_id": False})["sprinkle_2"]["is_auto"]
            is_active_1 = collection.find_one({"name": "sprinkle"}, {"_id": False})["sprinkle_1"]["is_activate"]
            is_active_2 = collection.find_one({"name": "sprinkle"}, {"_id": False})["sprinkle_2"]["is_activate"]
            if moisture_default - moisture >= 100 and is_active_1 == True:
                collection.update_one({"name": "sprinkle"}, {"$set": {"sprinkle_1":{"is_activate": True, "is_auto": False}}})
            elif moisture_default - moisture < 100 and is_active_1 == True:
                collection.update_one({"name": "sprinkle"}, {"$set": {"sprinkle_1":{"is_activate": True, "is_auto": False}}}) 
            elif moisture_default - moisture >= 100 and is_auto_1 == True:
                collection.update_one({"name": "sprinkle"}, {"$set": {"sprinkle_1":{"is_activate": True, "is_auto": False}}})
            elif moisture_default - moisture < 100 and is_auto_1 == True:
                collection.update_one({"name": "sprinkle"}, {"$set": {"sprinkle_1":{"is_activate": False, "is_auto": False}}})
            elif moisture_default - moisture >= 100 and is_active_2 == True:
                collection.update_one({"name": "sprinkle"}, {"$set": {"sprinkle_2":{"is_activate": True, "is_auto": False}}})
            elif moisture_default - moisture < 100 and is_active_2 == True:
                collection.update_one({"name": "sprinkle"}, {"$set": {"sprinkle_2":{"is_activate": True, "is_auto": False}}})
            elif moisture_default - moisture >= 100 and is_auto_2 == True:
                collection.update_one({"name": "sprinkle"}, {"$set": {"sprinkle_2":{"is_activate": True, "is_auto": False}}})
            elif moisture_default - moisture < 100 and is_auto_2 == True:
                collection.update_one({"name": "sprinkle"}, {"$set": {"sprinkle_2":{"is_activate": False, "is_auto": False}}})
            elif moisture_default - moisture >= 100 and is_active_2 == True:
                collection.update_one({"name": "sprinkle"}, {"$set": {"sprinkle_2":{"is_activate": False, "is_auto": False}}})
            else:
                collection.update_one({"name": "sprinkle"}, {"$set": {"sprinkle_1":{"is_activate": False, "is_auto": False}, 
                "sprinkle_2":{"is_activate": False, "is_auto": False}}})
                

        elif i["name"] == "buzzer-sunroof":
            buzzer = i["buzzer"]
            sunroof = i["sunroof"]
            if buzzer == True:
                collection.update_one({"name":"buzzer-sunroof"}, {"$set":{"buzzer": True, "sunroof": False}})
            elif buzzer == False:
                collection.update_one({"name":"buzzer-sunroof"}, {"$set":{"buzzer": False}})
            elif sunroof == True:
                collection.update_one({"name":"buzzer-sunroof"}, {"$set":{"sunroof": True}})
            elif sunroof == False:
                collection.update_one({"name":"buzzer-sunroof"}, {"$set":{"sunroof": False}})

    return {"message": "Garden is already update."}



@app.get("/garden/sprinkle")
def sprinkle():
    return collection.find_one({"name": "sprinkle"}, {"_id": False, "name": 0})


@app.get("/garden/moisture")
def moisture():
    return collection.find_one({"name": "moisture"}, {"_id": False, "name": 0, "moist_value": 0})


@app.get("/garden/buzzer-sunroof")
def buzzer_sunroof():
    return collection.find_one({"name": "buzzer-sunroof"}, {"_id": False, "name": 0})


@app.post("/update/moisture")
def update_moisture(moist_value: Moisture):
    moist_def = collection.find_one({"name": "moisture"})["moist_default"]
    collection.update_one({"name": "moisture"},{"$set": {"moist_value": moist_value.moisture_value, "moist_default": moist_def}})
    return {f"Moisture has been updated to {moist_value.moisture_value}"}


@app.post("/update/buzzer-sunroof")
def update_buzzer(buzzer:BuzzerSunroof):
    if buzzer.buzzer == True:
        collection.update_one({"name":"buzzer-sunroof"},{"$set":{"buzzer":buzzer.buzzer,"sunroof":False}})
        return {"status":f"Your buzzer is now {buzzer.buzzer} and your sunroof is now False"}
    elif buzzer.buzzer == False:
        collection.update_one({"name":"buzzer-sunroof"},{"$set":{"buzzer":buzzer.buzzer,"sunroof":buzzer.sunroof}})
        return {"status":f"Your buzzer is now {buzzer.buzzer} and your sunroof is now {buzzer.sunroof}"}