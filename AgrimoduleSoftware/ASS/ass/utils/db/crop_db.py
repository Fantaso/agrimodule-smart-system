# Automatically add crops to the db through SQLAlchemy
# in run.py directory
# 				from utils.db.crop_db import *

def add_crops(crops):
	print('Importing db and Crop')
	from solarvibes import db
	from solarvibes.models import Crop
	print('Starting inserting crops to db')
	for crop in crops:
		crop_to_db = Crop(**crops[crop])
		db.session.add(crop_to_db)
	db.session.commit()
	print('Crops added to db! Done!')


crops = {
	'green cardamom': {
		'characteristics': {
			'name':'green cardamom',
			'variety':'cardamom',
		 	'family':'dry fruit',
			'image': '',
			'yield':122.1153, # gr
			'canopy_x':30, # cm
			'canopy_y':30, # cm
			'canopy_z':300, # cm
			'density':2500, # plants/m2
			'fruit_quantity':610.5765,
			'fruit_size':7.6, # mm
			'fruit_weight':0.2, # gr
			'root_depth':45, # cm
			},
		'growth_stages': {
			'in_nursery': {
				'sowing': 1, # week
				'germination': 33, # week
				},
			'in_field': {
			 	'transplantation': 1, # week
				'vegetative_growth': 76, # week
				'fruit_development': 8, # week
				'maturity': 8, # week
				'harvest':4, # week
				},
			},
		'soil_characteristics': {
			'soil': {
			 	'preferences': 'loamy forest soils', #
				},
			'temperature': {
			 	'min': 10, # celcius
				'opt': 18, #
				'max': 35, #
				},
			'moisture': {
			 	'min': 45, # % moisture
				'opt': 48, #
				'max': 50, #
				},
			'ph': {
			 	'min': 4.5, # potential hydrogen - acidicity /alkaline
				'opt': 6.5, #
				'max': 7, #
				},
			'ec': {
			 	'min': 0, # electrical conductivity - salinity
				'opt': 0, #
				'max': 0, #
				},
			},
		'weather_characteristics': {
			'weather': {
			 	'preferences': 'forest weather, humid, normally grown under other bigger crops', #
				},
			'temperature': {
			 	'min': 10, # celcius
				'opt': 18, #
				'max': 35, #
				},
			'humidity': {
			 	'min': 60, # % relative humidity
				'opt': None, #
				'max': 75, #
				},
			'light': {
			 	'min': 8, # amount of light hours or solar radiation
				'opt': None, #
				'max': 12, #
				},
			'radiation': {
			 	'min': None, # watts/m2 or MJoules/day etc amount of light hours or solar radiation
				'opt': None, #
				'max': None, #
				},
			},
		'cropping_pattern': {
			'general': {
			 	'layout': 'east-west', # directions of plantations
				'layout_degree': 90, # degrees tor directions of layout
				},
			 'seeding': {
 			 	'location': 'nursery', #
 				'seed_quantity': 40, # gr / bed
				'bed_characteristics': {
    			 	'height': 0.2, # m
    				'width': 1, # m
   					'length': 6, # m
    				},
				'planting_space': {
    			 	'plant_space': 0., # m
    				'row_space': 0.1, # m
    				},
 				},
			'monoculture': {
			 	'single_row': {
				 	'plant_distance': 2, # m
					'row_distance': 2, # m
					},
				}
			},
		},
	}



# TO ADD THESE CROP DATASETS RUN:
# if __name__ == '__main__':
# 	add_crops(crops)
