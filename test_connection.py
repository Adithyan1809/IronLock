
import os
import ssl
import certifi

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

print("OpenSSL:", ssl.OPENSSL_VERSION)
print("Certifi:", certifi.where())

try:
    client = MongoClient(
        MONGO_DB_URL,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000
    )

    # Force an actual connection
    client.admin.command("ping")

    print("MongoDB connection successful!")

except Exception as e:
    print("MongoDB connection failed!")
    print(type(e).__name__)
    print(e)

finally:
    if "client" in locals():
        client.close()
