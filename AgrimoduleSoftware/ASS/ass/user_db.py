from ass import db, User, Role

users = { 	
			'carlos':
					{
					'name':'Carlos'
				    'last_name':'Rosas'
				    'email':'cmrhsv@gmail.com'
				    'password':'cmrhsv'
				    'birthday':''
				    'mobile':'+4917647645375'
					},
			'swathish': 
					{
					'name':'Swathish'
				    'last_name':'Ravi'
				    'email':'swathish.ravi@gmail.com'
				    'password':'swathish.ravi'
				    'birthday':''
				    'mobile':'+4917587878787'
					},
			'mansoor':
					{
					'name':'Mohgul'
				    'last_name':'Mansoor'
				    'email':'mohgul.mansoor@gmail.com'
				    'password':'mohgul.mansoor'
				    'birthday':''
				    'mobile':'+4917655252526'
					}, 
			'viktor':
					{
					'name':'Viktor'
				    'last_name':'Veeser'
				    'email':'viktor.veeser@gmail.com'
				    'password':'viktor.veeser'
				    'birthday':''
				    'mobile':'+4917545123695'
					},
			'pavarthi':
					{
					'name':'Pavarthi'
				    'last_name':'Radja'
				    'email':'pavarthi.radja@gmail.com'
				    'password':'pavarthi.radja'
				    'birthday':''
				    'mobile':'+491765848596'
					},
			'oscar':
					{
					'name':'Oscar'
				    'last_name':'Guerrero'
				    'email':'oscar.guerrero@gmail.com'
				    'password':'oscar.guerrero'
				    'birthday':''
				    'mobile':'+4917455668891'
					},
			'vera':
					{
					'name':'Vera'
				    'last_name':'Anna'
				    'email':'vera.anna@gmail.com'
				    'password':'vera.anna'
				    'birthday':''
				    'mobile':'+4917455668899'
					},
		}

# Automatically add users to the db through SQLAlchemy
def add_users(users):
	print('Starting inserting users to db')
	for user in users:
		user_to_db = User(**users[user])
		db.session.add(user_to_db)
	db.session.commit()
	print('Users added to db! Done!')


# TO ADD THESE CROP DATASETS RUN:
if __name__ == '__main__':
	add_users(users)