import sys
import pymongo 
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')

db = client.img_database
collection = db.img_collection

img_name = sys.argv[1]
img_width = int(sys.argv[2])
img_height = int(sys.argv[3])
img_size = int(sys.argv[4])

if img_name.endswith('.jpg'):
	img_name = img_name[:-4]

collection.insert({"imagename":img_name, "width":img_width, "height":img_height, "size":img_size})