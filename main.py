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
    moist_value: float
    moist_default: float
    sprinkle1: Sprinkle
    sprinkle2: Sprinkle
    buzzer: bool
    sunroof: bool


def moisture_to_percentage(moisture):
    percentage = round((moisture/1023)*100,2)
    return percentage

def percentage_to_moisture(percentage):
    percentage = round((percentage/100)*1023,2)
    return percentage


@app.get("/")
def read_root():
    return {"Hello": "Welcome to my little garden."}


@app.get("/garden/all")
def read_all_garden():
    data = collection.find({}, {"_id": False})


@app.post("/garden/update")
def update_garden(data: Body()):
    for item in collection.find({}, {"_id": False}):
        name = item["name"]
        if name == "moisture":
            is_auto = item.get("is_auto", False)
            is_active = item.get("is_active", False)
            if is_auto or is_active:
                collection.update_one({"": "moisture"}, percentage_to_moisture({"$set": {"moisture_default": int(moisture_default)}}))

        elif name == "sprinkle":
            is_auto = item["is_auto"]
            is_active = item["is_active"]
            if is_auto and is_active:
                collection.update_one({"": "moisture"}, percentage_to_moisture({"$set": {"moisture_default": int(moisture_default)}}))

        elif name == "buzzer-sunroof":
            buzzer = item["buzzer"]
            sunroof = item["sunroof"]
            update_dict = {}
            if buzzer:
                update_dict["buzzer"] = True
                update_dict["sunroof"] = False
            elif sunroof:
                update_dict["sunroof"] = True
            collection.update_one({"":"buzzer-sunroof"}, {"$set": update_dict})

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