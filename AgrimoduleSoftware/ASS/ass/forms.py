from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, Form, FormField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length

# Constructor
class PreContactUsForm:
	def __init__(self, name, email, phone, msg):
		self.name = name
		self.email = email
		self.phone = phone 
		self.msg = msg


# field enclosures - can
class PhoneForm(Form):
	country_code = IntegerField(label='Country Code:') 
	area_code = IntegerField(label='Area Code:') 
	number = IntegerField(label='Number:') 


class ContactUsFormEG(FlaskForm):
    name 	= StringField(label='Fullname',
    						validators=[
    								DataRequired(),
    								Length(min=3, max=30, message=None)])
    email 	= StringField('Email',
    						validators=[
    								DataRequired(),
    								Length(min=5, max=30, message=None),
    								Email()])
    phone 	= StringField('Phone',
    						validators=[
    								DataRequired(),
    								Length(min=7, max=30, message=None)])
    msg 	= TextAreaField	('Message',
    						validators=[
    								DataRequired(),
    								Length(min=-1, max=1000, message='Maximum characters: 1000')])
    # Inherits from PhoneForm the fields that are there
    home_phone 	= FormField(PhoneForm)
    handy_phone	= FormField(PhoneForm)
    work_phone	= FormField(PhoneForm)


# ContactUsFormExtended inherits all fields from ContactUsForm
class ContactUsFormExtended(ContactUsFormEG):
	city	= StringField(label='City',
							validators=[
									DataRequired()])
	country = StringField(label='Country',
							validators=[DataRequired()])

class ContactUsFormExtendedOne(ContactUsFormEG):
	start_date = DateField(label='Start Date', format='%Y-%m-%d')
# SNIPETS
# default='Carlos' # an atribute that can be pass inside the Field() of FlaskForm


# WEBSITE FORMS
# Templates
class EmailForm(FlaskForm):
	email 	= StringField('Email',
    						validators=[
    								DataRequired(),
    								Length(min=5, max=30, message=None),
    								Email()])

class EmailAndTextForm(EmailForm):
	msg   = TextAreaField('Message', validators=[DataRequired(), Length(min=-1, max=1000, message='Maximum characters: 1000')])


# Forms
class NewsletterForm(Form):
	pass
	# email = FormField(EmailForm)
	# msg = FormField(TextForm)

class AgrimoduleFBForm(Form):
	pass
	# email = FormField(TextForm)
	# msg = FormField(TextForm)

class PlatformFBForm(Form):
	pass
	# email = FormField(TextForm)
	# msg = FormField(TextForm)

class WorkWithUsForm(Form):
	pass
	# email = FormField(TextForm)
	# msg = FormField(TextForm)

class ContactUsForm(FlaskForm):
    name 	= StringField(label='Fullname',
    						validators=[
    								DataRequired(),
    								Length(min=3, max=30, message=None)])
    email 	= StringField('Email',
    						validators=[
    								DataRequired(),
    								Length(min=5, max=30, message=None),
    								Email()])
    phone 	= StringField('Phone',
    						validators=[
    								DataRequired(),
    								Length(min=7, max=30, message=None)])
    msg   = TextAreaField('Message',
    						validators=[
    								DataRequired(),
    								Length(min=-1, max=1000, message='Maximum characters: 1000')])


# SET UP FARM FORMS

# SET UP AGRIMODULE FORMS





