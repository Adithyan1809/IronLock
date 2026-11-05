
import os
import certifi
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

client = pymongo.MongoClient(
    MONGO_DB_URL,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000
)

try:
    client.admin.command("ping")
    print("MongoDB connection successful!")

except Exception as e:
    print("MongoDB connection failed:")
    print(e)

finally:
    client.close()
