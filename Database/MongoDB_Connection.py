import traceback

from pymongo import errors
from pymongo import MongoClient


def start_db():

    try:

        conn_string = "mongodb://localhost:27017/"
        client = MongoClient(conn_string)
        print(client.list_database_names())

        db = client["C964_Database"]
        collection = db["Finance_Data"]

        if collection.find_one({"symbol": "TESTSYMBOL"}):
            print("Test entry exists")
        else:
            print("Adding new test entry to database.")
            collection.insert_one(
                {"symbol": "TESTSYMBOL", "current": 211.58, "previous_close": 211.45, "market_cap": 3160000000000,
                 "volume": 32276821, "RSI": 61.30, "MACD": 18.35, "EMA": 336.02, "SMA": 211.75,
                 "Overall_Sentiment": 0.7})
        return db

    except errors.ConnectionFailure as e:
        print(f"Error connecting to database: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        return None


def close_db():
    conn_string = "mongodb://localhost:27017/"
    client = MongoClient(conn_string)
    client.close()
    print("Database connection closed.")
