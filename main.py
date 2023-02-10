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


def moisture_to_percentage(moisture):
    percentage = round((moisture/1023)*100, 2)
    return percentage


def percentage_to_moisture(percentage):
    percentage = round((percentage/100)*1023, 2)
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
        "moist_default": moisture_to_percentage(moist["moist_defualt"]),
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
def update_garden():
    collection.update_one({"name": "moisture"}, {"$set": {"is_active": False}})
    return {"message": "All garden is inactive."}


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
