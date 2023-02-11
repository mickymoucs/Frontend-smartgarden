from fastapi import APIRouter
from .garden import Moisture, BuzzerSunroof
from database.mongo_connection import *

router = APIRouter(
    prefix="/update",
    tags=["update"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/moisture")
def update_moisture(moist_value: Moisture):
    moist_def = collection.find_one({"name": "moisture"})["moist_default"]
    collection.update_one(
        {"name": "moisture"},
        {
            "$set": {
                "moist_value": moist_value.moisture_value,
                "moist_default": moist_def,
            }
        },
    )
    return {f"Moisture has been updated to {moist_value.moisture_value}"}


@router.post("/buzzer-sunroof")
def update_buzzer(buzzer: BuzzerSunroof):
    if buzzer.buzzer == True:
        collection.update_one(
            {"name": "buzzer-sunroof"},
            {"$set": {"buzzer": buzzer.buzzer, "sunroof": False}},
        )
        return {
            "status": f"Your buzzer is now {buzzer.buzzer} and your sunroof is now False"
        }
    elif buzzer.buzzer == False:
        collection.update_one(
            {"name": "buzzer-sunroof"},
            {"$set": {"buzzer": buzzer.buzzer, "sunroof": buzzer.sunroof}},
        )
        return {
            "status": f"Your buzzer is now {buzzer.buzzer} and your sunroof is now {buzzer.sunroof}"
        }
