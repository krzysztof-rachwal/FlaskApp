from pymongo import MongoClient
from collections import defaultdict
import password
import json
import os

# PASSOWRD FILE NOT INCUDED IN THE PROJECT FILES.

# for command line: 
# mongo --ssl --host csmongo.cs.cf.ac.uk -u scmle1 scmle1 -p

# with pymongo: 
# client = pymongo.MongoClient('mongodb://user_name:user_password@SERVER_IP/prod-db')

# start a mongodb client
client = MongoClient(f'mongodb://c1968648:{password.PASSWORD}@csmongo.cs.cf.ac.uk:27017/c1968648',ssl=True)

# create an object of the database
db = client.c1968648

# reinitialize the examples collection every time this script is executed
db.examples.delete_many({})


def load_imdb_data(data_folder):
	# d = {}
	d = defaultdict(list)
	files = os.listdir(data_folder)
	for one_file in files:
		f = open(os.path.join(data_folder,one_file),'r', encoding = 'utf8')
		#with open(os.path.join(data_folder,one_file),'r', encoding = 'utf8') as f:
		for infile in f:
			# process the review file 'f' and populate the dictionary 'd'
			d[one_file].append(infile)
			# d[one_file] = infile
	return d


train_data_folder = '20news/train'
test_data_folder = 'imdb/test'

train_data = load_imdb_data(train_data_folder)
test_data = load_imdb_data(test_data_folder)

print(type(train_data))
# print(list(train_data.keys())[0])
# print(train_data['pos'])


to_json = json.dumps(train_data)
# print(to_json)

with open('news.json', 'w') as json_file:
    json.dump(train_data, json_file)


data = json.load(open('news.json'))
# for keys, values in train_data.items():
# 	print(keys)
# 	print(values)

input('=== Press <ENTER> to insert documents ===')

# db.examples.insert_many(data)
# db.examples.insert_one(data)
for d in data:
	# print('Inserting: ',d)
	db.examples.insert_one(d)
print('\nDone!\n')


# input('=== EXAMPLE 1: Searching arrays containing string values===')
# query = {'values':'array_value1'}
# print('Query: ',query),input()
# res = list(db.examples.find(query))
# print('Found this: ')
# for r in res:
# 	print(r)

# input('\n--- Done! ---\n')

# input('=== EXAMPLE 2: Use the $in operator to search for multiple values in arrays===')
# query = {'values':{'$in':['array_value3',4]}}
# print('Query: ',query),input()
# res = list(db.examples.find(query))
# print('Found this: ')
# for r in res:
# 	print(r)

# input('\n--- Done! ---\n')

# input('=== EXAMPLE 3: Use the $all operator to search exact matches for multiple values in arrays===')
# query = {'values':{'$all':['array_value3',4]}}
# print('Query: ',query),input()
# res = list(db.examples.find(query))
# print('Found this: ')
# for r in res:
# 	print(r)

# input('=== EXAMPLE 4: Use dot notation to search for nested values===')
# query = {'values.nested_values':{'$gt':2}}
# print('Query: ',query),input()
# res = list(db.examples.find(query))
# print('Found this: ')
# for r in res:
# 	print(r)

