# Automatically add crops to the db through SQLAlchemy
# in run.py directory
# 				from utils.db.crop_db import

from datetime import datetime, timedelta, timezone

Class CropDB():


	"""this class contains the CropDB methods for everyhting related to the CropData:
	1. CROP CHARATERISTICS
	2. CROP IRRIGATION SCHEDULE
	3. CROP FERTILIZATION SCHEDULE"""

	def __init__(self, crop_name):
		""""this method initiates the crop variables to know
		which crop is the one that needs to get the calculations"""

		self.crop_name = crop_name

	def __repr__(self):
		""""this method returns the object representation of this class"""

		return "{}({})".format(self.__class__.__name__, self.crop_name)


	def add_crops(crops):
		""""this method will be used to add all the crops in here to the
		when and if created in localhost"""

		#  //TODO: the imports must be changed
		print('Importing db and Crop')
		from solarvibes import db
		from solarvibes.models import Crop
		print('Starting inserting crops to db')
		for crop in crops:
			crop_to_db = Crop(**crops[crop])
			db.session.add(crop_to_db)
		db.session.commit()
		print('Crops added to db! Done!')


	def get_rel_path(filename):
		""""this method gets the relative path of the object and join
		the relative path and the filename"""
		import os
		dirname = os.path.dirname(__file__)
		folder = 'images'
		url = os.path.join(dirname, folder, filename)
		return url








# TO ADD THESE CROP DATASETS RUN:
# if __name__ == '__main__':
# 	add_crops(crops)
