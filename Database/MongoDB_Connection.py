from pymongo import errors
from pymongo import MongoClient

try:
    conn_string = "mongodb://localhost:27017/"
    client = MongoClient(conn_string)
    print(client.list_database_names())

    db = client["C964_Database"]
    collection = db["Finance_Data"]

    if collection.find_one({"symbol": "TESTSYMBOL"}):
        print("Entry exists")

    else:
        collection.insert_one(
            {"symbol": "TESTSYMBOL", "current": 211.58, "previous_close": 211.45, "market_cap": 3160000000000,
             "volume": 32276821, "RSI": 61.30, "MACD": 18.35, "EMA": 336.02, "SMA": 211.75, "Overall_Sentiment": 0.7})

except errors.ConnectionFailure as e:
    print(f"Error connecting to database: {e}")

