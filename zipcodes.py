from pymongo import MongoClient
import pprint
import re

client = MongoClient("mongodb://localhost:27017")
db = client.test

'''MongoDB Exploring Functions'''
# Function returns top occuring 'limit' number of zip codes
def find_zips(limit):
    zipcodes = db.austin_texas.aggregate([
        {"$match": {"address.postcode": {"$exists": 1}}},
        {"$group": {"_id": "$address.postcode", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ])

    print("\n- Top " + str(limit) + " Occurring Zip Codes -")
    pprint.pprint([doc for doc in zipcodes])

# Function returns number of addresses with postcode field
def count_zips():
    num_zips = db.austin_texas.aggregate([
        {"$match": {"address.postcode": {"$exists": 1}}},
        {"$group": {"_id": "num_postcode", "count": {"$sum": 1}}}
    ])

    print("\n- Number of Addresses with a Postcode Field -")
    pprint.pprint(list(num_zips))

# Return zipcodes that are strings due to the a hyphen or other
# non-numerical value in the field
def find_zip_errors():
    str_zips = db.sample_20.aggregate([
        {"$match": {"address.postcode": {"$type": "string"}}},
        {"$project": {"_id": "$address"}}
    ])

    print("\n- Addresses that have Strings in Postcode Field -")
    pprint.pprint([doc for doc in str_zips])

# Return 'limit' number of documents that have an address but no zip code
def find_no_zips(limit):
    no_zips = db.sample_20.aggregate([
        {"$match": {"address.housenumber": {"$exists": 1},
                    "address.postcode": {"$exists": 0}}},
        {"$project": {"_id": "$address"}},
        {"$limit": limit}
    ])

    print("\n- Sample of " + str(limit) + \
          " Addresses with no Postcode Field -")
    pprint.pprint([doc for doc in no_zips])

# Function returns number of addresses with no postcode field
def count_no_zips():
    num_no_zips = db.austin_texas.aggregate([
        {"$match": {"address.housenumber": {"$exists": 1},
                    "address.postcode": {"$exists": 0}}},
        {"$group": {"_id": "num_no_zips", "count": {"$sum": 1}}}
    ])

    print("\n- Number of Addresses with no Postcode Field -")
    pprint.pprint(list(num_no_zips))

'''Cleaning Functions for XML'''
# Function to verify attribute is postcode field
def is_zip(k_value):
    return k_value == "addr:postcode"

# Function to extract 5 digit zipcode
def update_zip(v_value):
    try:
        # Retrieve first digits as a string
        digits = re.findall(r'\d+', str(v_value))[0]
        # Return first 5 digits of sequence as an integer
        return int(digits[:5])

    except IndexError: # No digits in string
        return v_value

if __name__ == '__main__':
    #find_zips(100)
    count_zips()
    #find_zip_errors()
    #find_no_zips(5)
    count_no_zips()