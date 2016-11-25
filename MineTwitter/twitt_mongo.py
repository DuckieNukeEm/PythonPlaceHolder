########
#
#This packages contains all the functions needed to  operate with mongodb and twitter api
#
#######

#Loading required packages
import json
import pymongo

def save_to_mongo(data, mongo_db, mongo_db_Coll, **mongo_conn_kw):
	#connects to the mongoDB server running on
	#localhost:270127 by default

	client = pymongo.MongoClient(**mongo_conn_kw)

	#Get a  refrence to a particular database

	db = client[mongo_db]

	#refrence a particual colection in the database

	coll = db[mongo_db_coll]

	#perform a bulk insert and return the IDs

	return coll.insert(data)

def load_from_mongo(mongo_db, mongo_db_coll, return_cursor = False, criteria = None, 
			projection = None, **mongo_conn_kw):
	# Optionally, use criteria and projection to limit the data that is
	# returned as documented in
	# http://docs.mongodb.org/manual/reference/method/db.collection.find/
	# Consider leveraging MongoDB's aggregations framework for more
	# sophisticated queries.
	client = pymongo.MongoClient(**mongo_conn_kw)
	db = client(mongo_db]
	coll = db[mongo_db_coll]

	if criteria is None:
		criteria = {}

	if projection is None:
		curosr = coll.find(criteria)
	else:
		cursor = coll.find(critera, projection)

	#returning a curos is recommended for large amounts of data

	if return_curosr:
		return cursor
	else:
		return[item for item in cursor]
