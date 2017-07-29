from pymongo import MongoClient
import pprint
from decimal import Decimal

client = MongoClient("mongodb://localhost:27017")
db = client.test

'''MongoDB Exploring Functions'''
# Function displays 'size' number of building addresses and heights
def sample_buildings(size):
    buildings = db.sample_20.aggregate([
        {"$match": {"building": "yes", "height": {"$exists": 1}, "address": {"$exists": 1}}},
        {"$project": {"_id": {"$concat": ["$address.housenumber", " ", "$address.street"]},
                      "building_height": "$height"}},
        {"$limit": size}
    ])

    print("\n- Sample of " + str(size) + " Buildings -")
    pprint.pprint([doc for doc in buildings])

# Function displays total number of buildings with addresses in the data
def count_buildings():
    num_buildings = db.austin_texas.aggregate([
        {"$match": {"building": "yes", "height": {"$exists": 1}, "address": {"$exists": 1}}},
        {"$group": {"_id": "num_buildings", "count": {"$sum": 1}}}
    ])

    print("\n- Number of Buildings -")
    pprint.pprint(list(num_buildings))

# Function displays 'size' number of the tallest and shortest buildings
def tallest_shortest(size):
    tallest_buildings = db.austin_texas.aggregate([
        {"$match":{"building": "yes", "height": {"$exists": 1}, "address": {"$exists": 1}}},
        {"$project": {"_id": {"$concat": ["$address.housenumber", " ", "$address.street"]},
                      "building_height": "$height"}},
        {"$sort": {"building_height": -1}},
        {"$limit": size}
    ])

    shortest_buildings = db.austin_texas.aggregate([
        {"$match": {"building": "yes", "height": {"$exists": 1}, "address": {"$exists": 1}}},
        {"$project": {"_id": {"$concat": ["$address.housenumber", " ", "$address.street"]},
                      "building_height": "$height"}},
        {"$sort": {"building_height": 1}},
        {"$limit": size}
    ])

    print("\n- Top " + str(size) + " Tallest Building Heights -")
    pprint.pprint([doc for doc in tallest_buildings])

    # Need to find smallest value to determine appropriate unit
    print("\n- Top " + str(size) + " Shortest Building Heights -")
    pprint.pprint([doc for doc in shortest_buildings])

'''Cleaning Functions for XML'''
# Function for determining if value is convertible to an float.
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Function for determining if value is convertible to an int.
def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

# Function to check if k-value of tag is "height"
def is_height(attrib):
    return attrib == "height"

# Function for updating all heights to have only 2 decimal places.
def update_height(value):
    return float(round(Decimal(value),2))

if __name__ == '__main__':
    #sample_buildings(10)
    #count_buildings()
    tallest_shortest(5)