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
    pass

@app.get("/garden/{name}")
def sprinkle():
    return list(collection.find({"name": "sprinkle"}))


@app.get("/garden/{name}")
def moisture():
    return list(collection.find({"name": "moisture"}))

@app.get("/garden/{name}")
def buzzer():
    return list(collection.find({"name": "buzzer-sunroof"}))

@app.post("/update/{name}")
def update_sprinkle(name: str, value: int):
    pass

@app.post("/update/{name}")
def update_moisture(name: str, value: int):
    pass

@app.post("/update/{name}")
def update_buzzer(name: str, value: int):
    pass



