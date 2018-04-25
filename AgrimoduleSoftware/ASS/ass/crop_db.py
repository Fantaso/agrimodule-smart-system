from ass import db, Crop

def calc_density(crop):
	density = (crops[crop]['space_x']) * (crops[crop]['space_y'])
	return density

def add_crop(*args, **kwargs):
	print (args)
	print ()
	print (kwargs)

crops = { 	'Plum':
					{ 
					'variety':'tomato',
				 	'family':'fruit',
					'yield':2.8,
					'space_x':0.25,
					'space_y':0.25,
					'density':'',
					'fruit_quantity':26,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'iceberg': 
					{
					'variety':'lettuce',
				 	'family':'leafy',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'arugula':
					{
					'variety':'',
				 	'family':'leafy',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					}, 

			'radicchio':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'bell_pepper':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'cabbage':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'coriander':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'basil':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'squash':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'chive':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'sweet_corn':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'black_bean':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'strawberry':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'tomato2':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'rice':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'chilli':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					},

			'cottom':
					{
					'variety':'',
				 	'family':'',
					'yield':,
					'space_x':,
					'space_y':,
					'density':'',
					'fruit_quantity':,
					'fruit_size':,
					'fruit_weight':,
					'water':,
					'nutrient':,
					'radiation':,
					'cycle_dtg_days':,
					'cycle_dtm_days':,
					'soil_ph_min':, 'soil_ph_opt':, 'soil_ph_max':,
					'soil_temp_min':,'soil_temp_opt':,'soil_temp_max':,
					'soil_humi_min':,'soil_humi_opt':,'soil_humi_max':,
					'soil_nutrient_min':,'soil_nutrient_opt':,'soil_nutrient_max':,
					'air_temp_min':,'air_temp_opt':,'air_temp_max':,
					'air_humi_min':,'air_humi_opt':,'air_humi_max':,
					}
		}
# id = db.Column(db.Integer, primary_key=True)
# _name = db.Column(db.String(25), unique=True, nullable=False)
# _variety = db.Column(db.String(25))
# _family = db.Column(db.String(25))
# _yield = db.Column(db.Float(precision=3))
# _space_x = db.Column(db.Float(precision=2))
# _space_y = db.Column(db.Float(precision=2))
# _density = db.Column(db.Float(precision=2))
# # FRUITS EACH PLANT
# _fruit_quantity = db.Column(db.Integer)
# _fruit_size = db.Column(db.Float(precision=2))
# _fruit_weight = db.Column(db.Float(precision=2))
# # RESOURCES REQUIRED
# _water = db.Column(db.Float(precision=4))
# _nutrient = db.Column(db.Float(precision=4))
# _radiation = db.Column(db.Float(precision=4))
# # CYCLE
# _cycle_dtg_days = db.Column(db.Integer)
# _cycle_dtm_days = db.Column(db.Integer)
# # REQUIREMENTS
# # SOIL
# _soil_ph_min = db.Column(db.Float(precision=2))
# _soil_ph_opt = db.Column(db.Float(precision=2))
# _soil_ph_max = db.Column(db.Float(precision=2))

# _soil_temp_min = db.Column(db.Float(precision=2))
# _soil_temp_opt = db.Column(db.Float(precision=2))
# _soil_temp_max = db.Column(db.Float(precision=2))

# _soil_humi_min = db.Column(db.Float(precision=2))
# _soil_humi_opt = db.Column(db.Float(precision=2))
# _soil_humi_max = db.Column(db.Float(precision=2))

# _soil_nutrient_min = db.Column(db.Float(precision=2))
# _soil_nutrient_opt = db.Column(db.Float(precision=2))
# _soil_nutrient_max = db.Column(db.Float(precision=2))
# # AIR
# _air_temp_min = db.Column(db.Float(precision=2))
# _air_temp_opt = db.Column(db.Float(precision=2))
# _air_temp_max = db.Column(db.Float(precision=2))

# _air_humi_min = db.Column(db.Float(precision=2))
# _air_humi_opt = db.Column(db.Float(precision=2))
# _air_humi_max = db.Column(db.Float(precision=2))
