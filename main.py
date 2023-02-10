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
    return list(collection.find())

@app.post("/garden/update")
def update_garden():
    collection.update_one({"name": "moisture"}, {"$set": {"is_active": False}})
    return {"message": "All garden is inactive."}

@app.get("/garden/sprinkle")
def sprinkle():
    return list(collection.find({"name": "sprinkle"}))

@app.get("/garden/moisture")
def moisture():
    return collection.find_one({"name":"moisture"},{"_id":False})

@app.get("/garden/buzzer-sunroof")
def buzzer():
    return collection.find_one({"name":"buzzer-sunroof"},{"_id":False})

@app.post("/update/moisture")
def update_moisture(moisture_value:int):
    collection.update_one({"name": "moisture"},{"$set": {"moisture_value": moisture_value}})
    return {f"Moisture has been updated to {moisture_value}"}

@app.post("/update/buzzer-sunroof")
def update_buzzer(buzzer:BuzzerSunroof):
    if buzzer.buzzer == True:
        collection.update_one({"name":"buzzer-sunroof"},{"$set":{"buzzer":buzzer.buzzer,"sunroof":False}})
        return {"status":f"Your buzzer is now {buzzer.buzzer} and your sunroof is now False"}
    elif buzzer.buzzer == False:
        collection.update_one({"name":"buzzer-sunroof"},{"$set":{"buzzer":buzzer.buzzer,"sunroof":buzzer.sunroof}})
        return {"status":f"Your buzzer is now {buzzer.buzzer} and your sunroof is now {buzzer.sunroof}"}


