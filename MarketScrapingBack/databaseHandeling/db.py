from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.websiteDatabase
collect = db.website_collection
tayara = {"url" : "https://www.tayara.tn/c/v%C3%A9hicules"}
result =collect.insert(tayara)