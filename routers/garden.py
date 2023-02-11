from fastapi import Body, APIRouter
from pydantic import BaseModel
from database.mongo_connection import *

router = APIRouter(
    prefix="/garden",
    tags=["garden"],
    responses={404: {"description": "Not Found"}},
)


class Moisture(BaseModel):
    moisture_value: int


class Sprinkle(BaseModel):
    is_auto: bool
    is_activate: bool


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


@router.get("/all")
def read_all_garden():
    moist = collection.find_one({"name": "moisture"})
    sprink = collection.find_one({"name": "sprinkle"})
    buz_sun = collection.find_one({"name": "buzzer-sunroof"})
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
def update_garden(data: Data = Body()):
    old = collection.find({}, {"_id": False})
    moist = old[0]
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
        sunroof = collection.find_one({"name": "buzzer-sunroof"}, {"_id": False})[
            "sunroof"
        ]
        if new_data[i].is_auto is True:
            moist = collection.find({}, {"_id": False})[0]
            # if the moisture value lower than the moisture default, the sprinkle will activated.
            if moist["moist_default"] - moist["moist_value"] >= 10 and sunroof is True:
                collection.update_one(
                    {"name": "sprinkle"},
                    {"$set": {lst[i]: {"is_auto": True, "is_activate": True}}},
                )
            # if the moistur value is not approximate to moisture default, the sprinkle will continue activated.
            elif moist["moist_default"] - moist["moist_value"] >= 1 and sunroof is True:
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
def sprinkle():
    return collection.find_one({"name": "sprinkle"}, {"_id": False, "name": 0})


@router.get("/moisture")
def moisture():
    return collection.find_one(
        {"name": "moisture"}, {"_id": False, "name": 0, "moist_value": 0}
    )


@router.get("/buzzer-sunroof")
def buzzer_sunroof():
    return collection.find_one({"name": "buzzer-sunroof"}, {"_id": False, "name": 0})
