from ass import db, Field, Farm, User, Crop
from datetime import datetime, timedelta

user1='Oscar'
farm1='farm berlin'

crop1='plum'
crop2='arugula'
crop3='romaine'
crop4='radicchio'
# FOLLOW THIS PATH AND CREATE A FIELD FOR AN SPECIFIC FARM AND CROP
# osci = User.query.filter_by(name='Oscar').first()
# farm_osci = osci.farms.filter_by(name = 'farm berlin').first()
# crop1 = Crop.query.filter_by(_name = 'plum').first()
# field1 = Field(name='plumming',size=500, date_start=datetime(2018,4,25), date_finish=datetime(2018,5,20), _current_yield=50.333, farm=farm_osci)


fields = {
			crop1:
					{
					'crop': Crop.query.filter_by(_name = crop1).first(),
				    'size':500,
				    'date_start': datetime(2018, 4, 25),
				    'date_finish': ( datetime(2018, 4, 25) + timedelta(Crop.query.filter_by(_name = crop1).first()._dtg + Crop.query.filter_by(_name = crop1).first()._dtm) ),
				    '_current_yield':
				    				(Crop.query.filter_by(_name = crop1).first()._yield \
				    					* (500 / Crop.query.filter_by(_name = crop1).first()._density) ),
				    'crops':[Crop.query.filter_by(_name = crop1).first()],
				    'farm': User.query.filter_by(name=user1).first().farms.filter_by(name=farm1).first(),
				    },
			# crop2:
			# 		{
			# 		'crop': Crop.query.filter_by(_name = crop2).first(),
			# 	    'size':200,
			# 	    'date_start': datetime(2018, 4, 25),
			# 	    'date_finish': ( datetime(2018, 4, 25) + timedelta(Crop.query.filter_by(_name = crop2).first()._dtg + Crop.query.filter_by(_name = crop2).first()._dtm) ),
			# 	    '_current_yield':
			# 	    				(Crop.query.filter_by(_name = crop2).first()._yield \
			# 	    					* (500 / Crop.query.filter_by(_name = crop2).first()._density) ),
			# 	    'crops':'',
			# 	    'farm': User.query.filter_by(name=user1).first().farms.filter_by(name=farm1).first(),
			# 	    },
			# crop3:
			# 		{
			# 		'crop': Crop.query.filter_by(_name = crop3).first(),
			# 	    'size':200,
			# 	    'date_start': datetime(2018, 4, 25),
			# 	    'date_finish': ( datetime(2018, 4, 25) + timedelta(Crop.query.filter_by(_name = crop3).first()._dtg + Crop.query.filter_by(_name = crop3).first()._dtm) ),
			# 	    '_current_yield':
			# 	    				(Crop.query.filter_by(_name = crop3).first()._yield \
			# 	    					* (500 / Crop.query.filter_by(_name = crop3).first()._density) ),
			# 	    'crops':'',
			# 	    'farm': User.query.filter_by(name=user1).first().farms.filter_by(name=farm1).first(),
			# 	    },
			# crop1:
			# 		{
			# 		'crop': Crop.query.filter_by(_name = crop1).first(),
			# 	    'size':100,
			# 	    'date_start': datetime(2018, 4, 25),
			# 	    'date_finish': ( datetime(2018, 4, 25) + timedelta(Crop.query.filter_by(_name = crop1).first()._dtg + Crop.query.filter_by(_name = crop1).first()._dtm) ),
			# 	    '_current_yield':
			# 	    				(Crop.query.filter_by(_name = crop1).first()._yield \
			# 	    					* (500 / Crop.query.filter_by(_name = crop1).first()._density) ),
			# 	    'crops':'',
			# 	    'farm': User.query.filter_by(name=user1).first().farms.filter_by(name=farm1).first(),
			# 	    },
    	}


# Automatically add crops to the db through SQLAlchemy
def add_fields(fields, user):
	print( 'Starting inserting fields to db to user: {} in farm {}'.format(User.query.filter_by(name=user).first().name, User.query.filter_by(name=user).first().farms.filter_by(name=farm1).first()) )
	for field in fields:
		field_to_db = Field(**fields[field])
		db.session.add(field_to_db)
	db.session.commit()
	print('Fields added to db! Done!')


# due to db.session not handle in the app yet.  different methods cant be used to add automatically to the db.
# USE the random_user to the the user in a python repl session and then pass in the same session the random_user to add the farms
'''e.g.
		ru1 = get_user()
		ru2 = get_user()
		ru3 = get_user()
		ru4 = get_user()
		rus = [ru1, ru2, ru3, ru4]
		for ru in rus:
			add_farms(farms, ru) # farms come from the farm dictionary manual db'''

# def add_farm_with_user(farms):
# 	random_user = get_user()
# 	add_farms(farms, random_user)
# TO ADD THESE CROP DATASETS RUN:

if __name__ == '__main__':
	add_farms()