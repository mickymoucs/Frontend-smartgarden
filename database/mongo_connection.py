from pymongo import MongoClient
from dotenv import load_dotenv
import os

# get username and password from .env file
load_dotenv(".env")
username = os.getenv("username")
password = os.getenv("password")

client = MongoClient(
    f"mongodb://{username}:{password}@mongo.exceed19.online:8443/?authMechanism=DEFAULT"
)

# use database name "exceed08"
db = client["exceed08"]
# use collection name "my_little_garden"
collection = db["my_little_garden"]
