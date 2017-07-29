from pymongo import MongoClient
import pprint

client = MongoClient("mongodb://localhost:27017")
db = client.test

# Return the "limit" number of most occurring amenities
def find_amenities(limit):
    amenities = db.austin_texas.aggregate([
        {"$match": {"amenity": {"$exists": 1}}},
        {"$group": {"_id": "$amenity", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ])

    print("\n- Amenities -")
    pprint.pprint([doc for doc in amenities])

    # Nothing problematic about amenities

def find_streets():
    query = {"address.street" : { "$exists" : 1}}
    projection = {"_id" : 0, "address.street": 1}
    streets = db.sample_20.find(query, projection)
    street_type_dict = {}
    for street in streets:
        street_name = street.get('address').get('street')
        street_type = street_name.split()[-1]
        if street_type not in street_type_dict:
            street_type_dict[street_type] = 1
        else:
            street_type_dict[street_type] += 1

    street_types = db.street_types
    street_types.insert(street_type_dict)

    sorted_street_types = db.street_types.aggregate([
        {"$match": {"amenity": {"$exists": 1}}},
        {"$group": {"_id": "$amenity", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ])
    print("\n- Street Types -")
    pprint.pprint(street_type_dict)

    # A few abbreviations that can be changed over.

# Find all bars with opening hours
def find_bar_hours():
    bar_hours = db.austin_texas.aggregate([
        {"$match": {"amenity": "bar", "opening_hours": {"$exists": 1}}},
        {"$project": {"_id": "$name", "hours": "$opening_hours"}}
    ])

    print("\n- Bar Hours in Austin -")
    pprint.pprint([doc for doc in bar_hours])

if __name__ == '__main__':
    #find_amenities(5)
    #find_streets()
    find_bar_hours()