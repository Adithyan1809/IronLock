import os
import sys
import json
import certifi
from pymongo import MongoClient
import pandas as pd
import numpy as np

from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

ca = certifi.where()


class NetworkDataExtract():

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def cv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)

            data.reset_index(drop=True)

            records = list(
                json.loads(data.T.to_json()).values()
            )

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:

            self.mongo_client = MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )

            self.database = self.mongo_client[database]

            self.collection = self.database[collection]

            self.collection.insert_many(records)

            return (
                f"Data inserted successfully into "
                f"{database}.{collection}"
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)

        finally:
            if hasattr(self, "mongo_client"):
                self.mongo_client.close()


if __name__ == "__main__":

    FILE_PATH = "Network_Data/phisingData.csv"

    DATABASE = "NetworkSecurity"

    collection = "NetworkData"

    networkobj = NetworkDataExtract()

    records = networkobj.cv_to_json_convertor(
        file_path=FILE_PATH
    )

    no_of_records = networkobj.insert_data_mongodb(
        records=records,
        database=DATABASE,
        collection=collection
    )

    print(no_of_records)
