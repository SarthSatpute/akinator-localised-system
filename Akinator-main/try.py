from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["akinator_db"]
collection = db["friends"]

sample = collection.find_one()  # Get one document to inspect
print(sample)
