#!/usr/bin/env python3

import os
import json
import requests
from PIL import Image

target_path = './'

def update_from_camera(camera):
	camera = camera.upper()
	print("Updating from "+camera)

	dir_name = camera+'_JPEG'

	page = 0
	frame_n = 0

	if not os.path.exists(target_path+dir_name):
	    os.makedirs(target_path+dir_name)

	#https://mars.nasa.gov/rss/api/?feed=raw_images&category=mars2020,ingenuity&feedtype=json&ver=1.2&num=100&page=7&&order=sol+desc&&search=|HELI_NAV&&
	while True:
		r = requests.get('https://mars.nasa.gov/rss/api/?feed=raw_images&category=mars2020,ingenuity'
			+'&feedtype=json&ver=1.2&num=100&page={page}&&order=sol+desc&&search=|{camera}&&' \
			.format(page=page, camera=camera) )

		try:
			images = r.json()["images"]
		except KeyError as e:
			print(r.json())
			raise e  

		if len(images) == 0: 
			print('no updates')
			break
		
		print("page %d, %d images:"%(page, len(images)))
			
		_brk = False
		for img in images:	
			img_filename = target_path+dir_name+'/'+img["imageid"]+".jpg"

			if os.path.exists(img_filename):
				print("done")
				_brk = True
				break

			im = Image.open(requests.get(img["image_files"]["full_res"], stream=True).raw)
			im.save(img_filename, quality=90)
			im.close()
			print("  + %d   %s" % (frame_n, img["imageid"]))
			frame_n += 1
		if _brk: break	

		if frame_n % 100 == 0:
			page += 1	


update_from_camera("HELI_NAV")
update_from_camera("HELI_RTE")			
	