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
    moisture_default: int

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
    pass


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
    return list(collection.find({"name": "sprinkle"}))

@app.get("/garden/moisture")
def moisture():
    return list(collection.find({"name": "moisture"}))

@app.get("/garden/buzzer-sunroof")
def buzzer():
    return list(collection.find({"name": "buzzer-sunroof"}))

@app.post("/update/sprinkle")
def update_sprinkle(name: str, value: int):
    pass

@app.post("/update/moisture")
def update_moisture(name: str, value: int):
    pass

@app.post("/update/buzzer-sunroof")
def update_buzzer(name: str, value: int):
    pass