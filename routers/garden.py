from fastapi import Body, APIRouter
from pydantic import BaseModel
from database.mongo_connection import *
from typing import Dict

router = APIRouter(
    prefix="/garden",
    tags=["garden"],
    responses={404: {"description": "Not Found"}},
)


class Moisture(BaseModel):
    """Base class for moisture data."""
    moisture_value: int


class Sprinkle(BaseModel):
    """Base class for sprinkle status."""
    is_auto: bool
    is_activate: bool


class BuzzerSunroof(BaseModel):
    """Base class for buzzer and sunroof status."""
    buzzer: bool
    sunroof: bool


class Data(BaseModel):
    """Base class for all data."""
    moist_value: int
    moist_default: int
    sprinkle_1: Sprinkle
    sprinkle_2: Sprinkle
    buzzer: bool
    sunroof: bool


@router.get("/all")
def read_all_garden() -> Dict:
    """Get  and return all the data from the database."""
    # get moisture document in database.
    moist = collection.find_one({"name": "moisture"})

    # get sprinkle document in database.
    sprink = collection.find_one({"name": "sprinkle"})

    # get buzzer-sunroof document in database.
    buz_sun = collection.find_one({"name": "buzzer-sunroof"})

    # create new data for other to get from this endpoint.
    for_send = {
        "moist_value": moist["moist_value"],
        "moist_default": moist["moist_default"],
        "sprinkle_1": {
            "is_auto": sprink["sprinkle_1"]["is_auto"],
            "is_activate": sprink["sprinkle_1"]["is_activate"],
        },
        "sprinkle_2": {
            "is_auto": sprink["sprinkle_2"]["is_auto"],
            "is_activate": sprink["sprinkle_2"]["is_activate"],
        },
        "buzzer": buz_sun["buzzer"],
        "sunroof": buz_sun["sunroof"],
    }
    return for_send


@router.post("/update")
async def update_garden(data: Data = Body()) -> Dict:
    """Update the data from the body's data that send with the request."""
    # update the moisture default from user
    collection.update_one(
        {"name": "moisture"},
        {
            "$set": {
                "moist_default": data.moist_default,
                "moist_value": data.moist_value,
            }
        },
    )

    # update the buzzer and sunroof status
    if data.buzzer == True:
        collection.update_one(
            {"name": "buzzer-sunroof"},
            {"$set": {"buzzer": data.buzzer, "sunroof": False}},
        )
    elif data.buzzer == False:
        collection.update_one(
            {"name": "buzzer-sunroof"},
            {"$set": {"buzzer": data.buzzer, "sunroof": data.sunroof}},
        )

    # update sprinkles status
    new_data = [data.sprinkle_1, data.sprinkle_2]
    lst = ["sprinkle_1", "sprinkle_2"]
    for i in range(0, 2):
        sunroof = collection.find_one({"name": "buzzer-sunroof"}, {"_id": False})["sunroof"]
        if new_data[i].is_auto is True:
            moist = collection.find({}, {"_id": False})[0]
            # if the moisture value lower than the moisture default, the sprinkle will activated.
            if moist["moist_default"] - moist["moist_value"] >= 10:
                collection.update_one({"name": "buzzer-sunroof"}, {"$set": {"sunroof": True, "buzzer": False}})
                collection.update_one(
                    {"name": "sprinkle"},
                    {"$set": {lst[i]: {"is_auto": True, "is_activate": True}}},
                )
            # if the moistur value is not approximate to moisture default, the sprinkle will continue activated.
            elif moist["moist_default"] - moist["moist_value"] >= 1:
                collection.update_one({"name": "buzzer-sunroof"}, {"$set": {"sunroof": True, "buzzer": False}})
                collection.update_one(
                    {"name": "sprinkle"},
                    {"$set": {lst[i]: {"is_auto": True, "is_activate": True}}},
                )
            else:
                collection.update_one(
                    {"name": "sprinkle"},
                    {"$set": {lst[i]: {"is_auto": True, "is_activate": False}}},
                )
        elif new_data[i].is_auto is False:
            # If sunroof is true (open) sprinkle can on or off up to the condition.
            if sunroof is True:
                collection.update_one(
                    {"name": "sprinkle"},
                    {
                        "$set": {
                            lst[i]: {
                                "is_auto": False,
                                "is_activate": new_data[i].is_activate,
                            }
                        }
                    },
                )
            # If sunroof if false (off) sprinkle can not be activated.
            else:
                collection.update_one(
                    {"name": "sprinkle"},
                    {"$set": {lst[i]: {"is_auto": False, "is_activate": False}}},
                )
    return {"message": "Garden is already update."}


@router.get("/sprinkle")
def sprinkle() -> Dict:
    """Get and return sprinkles data."""
    return collection.find_one({"name": "sprinkle"}, {"_id": False, "name": 0})


@router.get("/moisture")
def moisture() -> Dict:
    """Get and return moisture data."""
    return collection.find_one(
        {"name": "moisture"}, {"_id": False, "name": 0, "moist_value": 0}
    )


@router.get("/buzzer-sunroof")
def buzzer_sunroof() -> Dict:
    """Get and return buzzer and sunroof data."""
    return collection.find_one({"name": "buzzer-sunroof"}, {"_id": False, "name": 0})
