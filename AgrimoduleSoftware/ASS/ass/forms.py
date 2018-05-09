from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, TextAreaField, Form, FormField, IntegerField, RadioField, SelectField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from flask_security.forms import RegisterForm, ConfirmRegisterForm
from flask_uploads import IMAGES

# WEBSITE FORMS
# Templates
class EmailForm(FlaskForm):
	email 	= StringField('Email',
    						validators=[
    								DataRequired(),
    								Length(min=5, max=30, message=None),
    								Email()])

class EmailAndTextForm(EmailForm):
	msg     = TextAreaField('Message',
                            validators=[
                                    DataRequired(),
                                    Length(min=-1, max=1000, message='Maximum characters: 1000')])

class ContactUsForm(EmailAndTextForm):
    name 	= StringField(label='Fullname',
    						validators=[
    								DataRequired(),
    								Length(min=3, max=30, message=None)])
    phone 	= StringField('Phone',
    						validators=[
    								DataRequired(),
    								Length(min=7, max=30, message=None)])
#Extended form for register flask-security
class RegisterFormExt(RegisterForm, ConfirmRegisterForm):
    name        = StringField(label='Name',
                            validators=[
                                    DataRequired(),
                                    Length(min=2, max=30, message='''Your name needs
                                                                        at least 2 characters.''')])
    last_name   = StringField(label='Last name',
                            validators=[
                                    DataRequired(),
                                    Length(min=2, max=30, message='''Your last name needs
                                                                        at least 2 characters.''')])
    birthday   = DateField(label='Birthday', format='%Y-%m-%d')
    mobile   = StringField('Mobile',
                            validators=[
                                    DataRequired(),
                                    Length(min=7, max=30, message=None)])

# SET UP FARM FORMS

# SET UP AGRIMODULE FORMS

class CultivationProcessForm(FlaskForm):
    cultivation_process     = SelectField(label='Cultivation Process',
                                    validators=[DataRequired()],
                                    choices=[('Organic','Organic'),('Chemical','Chemical')])

class CultivationTypeForm(FlaskForm):
    cultivation_type        = SelectField(label='Cultivation Type',
                                                validators=[DataRequired()],
                                                choices=[('mono','Mono'), ('mix','Mix'), ('multi','Multi')])
class CultivationStateForm(FlaskForm):
    cultivation_state       = SelectField(label='Cultivation State',
                                                validators=[DataRequired()],
                                                choices=[('new','New'),('Already Growing','Already Growing')])

class CultivationStartDateForm(FlaskForm):
    cultivation_start_date  = DateField(label='Cultivation Start Date', format='%Y-%m-%d',
                                                validators=[DataRequired()])

class CultivationCropForm(FlaskForm):
    cultivation_crop        = SelectField(label='Cultivation Crop',
                                                validators=[DataRequired()],
                                                choices=[('plum','Plum'),('romaine','Romaine'),('arugula','Arugula')],
                                                option_widget=None)

class CultivationAreaForm(FlaskForm):
    cultivation_area       = FloatField(label='Cultivation Area',
                                     validators=[DataRequired(),
                                                 NumberRange(min=5, max=5000, message='Area between 5 and 5000 m2')]) 


class FarmForm(CultivationAreaForm, CultivationProcessForm):
    name        = StringField(label='Farm name',
                            validators=[
                                    DataRequired(),
                                    Length(min=2, max=30, message='''Your name needs
                                                                        at least 2 characters.''')])
    location    = StringField(label='Farm location',
                            validators=[
                                    DataRequired(),
                                    Length(min=2, max=30, message='''Your name needs
                                                                        at least 2 characters.''')])

class FieldForm(FlaskForm):
    name                    = StringField(label='Field name',
                                                validators=[
                                                        DataRequired(),
                                                        Length(min=2, max=30, message='''Your name needs
                                                                                         at least 2 characters.''')])
    
    cultivation_area       = FloatField(label='Field Cultivation Area',
                                                validators=[DataRequired()],render_kw={"placeholder":"500.50"})

    cultivation_crop        = SelectField(label='Cultivation Crop',
                                                validators=[DataRequired()],
                                                choices=[('plum','Plum'),('romaine','Romaine'),('arugula','Arugula')])

    cultivation_start_date  = DateField(label='Cultivation Start Date', format='%Y-%m-%d',
                                                validators=[DataRequired()])
    cultivation_state       = SelectField(label='Cultivation State',
                                                validators=[DataRequired()],
                                                choices=[('new','New'),('already growing','Already Growing')])
    cultivation_type        = SelectField(label='Cultivation Type',
                                                validators=[DataRequired()],
                                                choices=[('mono','Mono'), ('mix','Mix'), ('multi','Multi')])

# Constructor
class PreUserProfileForm:
    def __init__(self, username, name, last_name, address, zipcode, city, state, country, email, email_rec, birthday, image, mobile):
        self.username    = username
        self.name        = name
        self.last_name   = last_name
        self.address     = address
        self.zipcode     = zipcode
        self.city        = city
        self.state       = state
        self.country     = country
        self.email       = email
        self.email_rec   = email_rec
        self.birthday    = birthday
        self.image       = image
        self.mobile      = mobile

class UserProfileForm(FlaskForm):
    username    = StringField('Username',           validators=[Length(min=2, max=30, message='Your Username needs to be at least 2 characters long.')])
    name        = StringField('Name',               validators=[Length(min=2, max=30, message='Your name needs to be at least 2 characters long.')])
    last_name   = StringField('Last name',          validators=[Length(min=2, max=30, message='Your last name needs to be at least 2 characters long.')])
    address     = StringField('Address',            validators=[Length(min=2, max=30, message='Minimum: 2 characters.')])
    zipcode     = StringField('Zipcode',            validators=[Length(min=1, max=7, message='Minimum: 1 characters.')])
    city        = StringField('City',               validators=[Length(min=6, max=30, message='Minimum: 2 characters.')])
    state       = StringField('State',              validators=[Length(min=2, max=30, message='Minimum: 2 characters.')])
    country     = StringField('Country',            validators=[Length(min=2, max=30, message='Minimum: 2 characters.')])
    email       = StringField('Email',              validators=[Length(min=5, max=30, message=None), Email()])
    email_rec   = StringField('Recovery Email',     validators=[Length(min=5, max=30, message=None), Email()])
    birthday    = DateField('Birthday',             format='%Y-%m-%d')
    image       = FileField(                        validators=[FileAllowed(IMAGES, 'Only images allowed.')])
    mobile      = StringField('Mobile',             validators=[Length(min=7, max=30, message=None)])




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
    name    = StringField(label='Fullname',
                            validators=[
                                    DataRequired(),
                                    Length(min=3, max=30, message=None)])
    email   = StringField('Email',
                            validators=[
                                    DataRequired(),
                                    Length(min=5, max=30, message=None),
                                    Email()])
    phone   = StringField('Phone',
                            validators=[
                                    DataRequired(),
                                    Length(min=7, max=30, message=None)])
    msg     = TextAreaField ('Message',
                            validators=[
                                    DataRequired(),
                                    Length(min=-1, max=1000, message='Maximum characters: 1000')])
    # Inherits from PhoneForm the fields that are there
    home_phone  = FormField(PhoneForm)
    handy_phone = FormField(PhoneForm)
    work_phone  = FormField(PhoneForm)


# ContactUsFormExtended inherits all fields from ContactUsForm
class ContactUsFormExtended(ContactUsFormEG):
    city    = StringField(label='City', validators=[
                                    DataRequired()])
    country = StringField(label='Country',
                            validators=[DataRequired()])

class ContactUsFormExtendedOne(ContactUsFormEG):
    start_date = DateField(label='Start Date', format='%Y-%m-%d')
# SNIPETS
# default='Carlos' # an atribute that can be pass inside the Field() of FlaskForm