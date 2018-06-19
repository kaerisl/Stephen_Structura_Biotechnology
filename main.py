#flask/MongoDB related
from flask import Flask, request, send_file
import pymongo 
from flask_pymongo import PyMongo
from pymongo import MongoClient

#OS related
from bson.json_util import dumps
import datetime
import psutil
import os

#image manipulation related
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage, misc
from scipy.ndimage.filters import gaussian_filter
from skimage.transform import rescale, resize, downscale_local_mean
import cv2

client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')

ti = datetime.datetime.now()
db = client.img_database
app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def index():
	collection = db.img_collection
	sub_col = collection.find()
	temp = ''
	for i in sub_col:
		temp = temp + i["imagename"] + ', ' 
	return temp[:-2]

@app.route('/list')
def list(max_width = -1,min_area = -1,min_bits_per_pix = -1):
	if request.args.get('max_width'):
		max_width = int(request.args.get('max_width'))
	if request.args.get('min_area'):
		min_area = int(request.args.get('min_area'))
	if request.args.get('min_bits_per_pix'):
		min_bits_per_pix = float(request.args.get('min_bits_per_pix'))

	collection = db.img_collection
	if max_width !=- 1:
		sub_col = collection.aggregate([ 
			{'$match': {'width' : { '$lte' : max_width} } },
			{'$project': { 'imagename': 1, 'area': {'$multiply':['$width','$height']} , 'size': 1} },
			{'$match': { 'area': {'$gte': min_area} } },
			{'$project': { 'imagename': 1, 'bits_per_pix': {'$multiply':[{'$divide':['$size','$area']},8 ]} } },
			{'$match': { 'bits_per_pix': {'$gte': min_bits_per_pix} } },
			])
	else:
		sub_col = collection.aggregate([ 
			{'$project': { 'imagename': 1, 'area': {'$multiply':['$width','$height']} , 'size': 1} },
			{'$match': { 'area': {'$gte': min_area} } },
			{'$project': { 'imagename': 1, 'bits_per_pix': {'$multiply':[{'$divide':['$size','$area']},8 ]} } },
			{'$match': { 'bits_per_pix': {'$gte': min_bits_per_pix} } },
			])
	temp = ''
	for i in sub_col:
		temp = temp + i["imagename"] + ', ' 
	return temp[:-2]

@app.route('/image/<imagename>/<filtertype>')
def image(imagename, filtertype):
	flag = 0
	log = db.log
	ts = datetime.datetime.now()

	filename='assets/'+imagename+'.jpg'
	img = misc.imread(filename)
	img[:] = np.max(img,axis=-1,keepdims=1)/2+np.min(img,axis=-1,keepdims=1)/2

	if filtertype == "greyscale":
		plt.imsave('test.jpg',img)
		flag=1

	elif filtertype == "lowpass" and request.args.get('value'):
		blurred = gaussian_filter(img, sigma = float(request.args.get('value')))
		plt.imsave('test.jpg',blurred)
		flag=1

	if filtertype == "crop":
		def crop_center(img,cropx,cropy):
			y,x,c = img.shape
			startx = x//2 - cropx//2
			starty = y//2 - cropy//2    
			return img[starty:starty+cropy, startx:startx+cropx]
		y,x,z = img.shape
		if y>x:
			cropped = crop_center(img,x,x)
		else:
			cropped = crop_center(img,y,y)
		plt.imsave('test.jpg',cropped)
		flag=1

	elif filtertype == "dx":
		sobelx = cv2.Sobel(img,cv2.cv2.CV_8U,1,0,ksize=5)
		plt.imsave('test.jpg',sobelx)
		flag=1

	if filtertype == "dy":
		sobely = cv2.Sobel(img,cv2.cv2.CV_8U,0,1,ksize=5)
		plt.imsave('test.jpg',sobely)
		flag=1

	elif filtertype == "downsample" and request.args.get('value'):
		downsampled = rescale(img, 1.0 / float(request.args.get('value')), anti_aliasing=False)
		plt.imsave('test.jpg',downsampled)
		flag=1

	if filtertype == "rotate" and request.args.get('value'):
		rotated = ndimage.rotate(img, int(request.args.get('value')))
		plt.imsave('test.jpg',rotated)
		flag=1

	te = datetime.datetime.now()
	if request.args.get('value') and flag == 1:
		log.insert({'imagename':imagename, 'cmd':filtertype, 'value':float(request.args.get('value')),'request_timestamp':str(ts),'processing_time':str(te-ts)})
	elif flag == 1:
		log.insert({'imagename':imagename, 'cmd':filtertype, 'value':'null','request_timestamp':str(ts),'processing_time':str(te-ts)})
	
	if flag == 1:
		return send_file('test.jpg',mimetype='image/gif')
	else:
		return 'Error Processing File'

@app.route('/dump')
def dump():
	os.system("mongodump --db img_collection --out dump")
	return ''

@app.route('/mem')
def mem():
	process = psutil.Process(os.getpid())
	mem_usage = process.memory_info().wset
	cpu_usage = process.cpu_percent()
	tm = datetime.datetime.now()
	return 'Current Memory Usage: ' + str(mem_usage) + 'B CPU Usage: ' + str(cpu_usage) + '% Uptime: '+ str(tm-ti)

@app.route('/log')
def log():
	log = db.log
	sub_col = db.log.find({'$query': {}, '$orderby': {'$natural' : -1}}).limit(100)
	return dumps(sub_col)

if __name__ == "__main__":
	app.run();