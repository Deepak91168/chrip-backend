from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

try:
    if config:
        print("Environment variables loaded successfully:")
        # for key, value in config.items():
        #     print(f"{key}={value}")
    else:
        print("No environment variables found in the .env file.")
except Exception as e:
    print(f"Error loading environment variables: {e}")


MONGO_URL = config.get("MONGODB_URL")

client = MongoClient(MONGO_URL)
db = client["Chirp"]
collection = db["users"]
print("connected to db")

