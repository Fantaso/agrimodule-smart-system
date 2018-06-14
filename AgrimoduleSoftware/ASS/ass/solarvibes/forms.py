from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, TextAreaField, Form, FormField, IntegerField, RadioField, SelectField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from flask_security.forms import RegisterForm, ConfirmRegisterForm
from flask_uploads import IMAGES


class PreAddPumpForm:
    def __init__(self, pump_name, pump_brand, pump_flow_rate, pump_head, pump_watts):
        self.pump_name       = pump_name
        self.pump_brand      = pump_brand
        self.pump_flow_rate  = pump_flow_rate
        self.pump_head       = pump_head
        self.pump_watts      = pump_watts

class AddPumpForm(FlaskForm):
    pump_name               = StringField('Pump name',                              validators=[DataRequired(), Length(min=2, max=30, message='Give it a name for sanity MAX 30.')])
    pump_brand              = StringField('Pump brand',                             validators=[DataRequired(), Length(min=2, max=30, message='Your pump supplier or brand name')])
    pump_flow_rate          = FloatField('Pump flow rate (liters per sec)',         validators=[DataRequired(), NumberRange(min=1, max=500, message="Your pump's water capacity or water turn over")])
    pump_head               = FloatField('Pump head (meters)',                      validators=[DataRequired(), NumberRange(min=1, max=500, message="Your pump's max head pressure or height power")])
    pump_watts              = FloatField('Pump power consumption (kilo Watts)',     validators=[DataRequired(), NumberRange(max=1000, message="Your pump's wattage consumption")])


#Extended form for register flask-security
class RegisterFormExt(RegisterForm, ConfirmRegisterForm):
    name        = StringField(label='Name', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    last_name   = StringField(label='Last name', validators=[DataRequired(), Length(min=2, max=30, message='''Your last name needs at least 2 characters.''')])
    birthday   = DateField(label='Birthday', format='%Y-%m-%d')
    mobile   = StringField('Mobile', validators=[DataRequired(), Length(min=7, max=30, message=None)])

class FarmForm(FlaskForm):
    farm_name                   = StringField('Farm name', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    farm_location               = StringField('Farm location', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    farm_area                   = FloatField('Farm Cultivation Area', validators=[DataRequired(), NumberRange(min=1, max=5000, message='Area between 1 and 5000 m2')])
    farm_cultivation_process    = SelectField('Farm Cultivation Process', validators=[DataRequired()], choices=[('Organic','Organic'),('Chemical','Chemical')])


class FieldForm(FlaskForm):
    field_name                    = StringField(label='Field name', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    field_cultivation_area       = FloatField(label='Field Cultivation Area', validators=[DataRequired(), NumberRange(min=1, max=5000, message='Cultivation area should be maximum as big as your farm')],render_kw={"placeholder":"500.50"})
    field_cultivation_crop        = SelectField(label='Cultivation Crop', validators=[DataRequired()], coerce = int)
    field_cultivation_start_date  = DateField(label='Cultivation Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    field_cultivation_state       = SelectField(label='Cultivation State', validators=[DataRequired()], choices=[('new','New'),('already growing','Already Growing')])
    field_cultivation_type        = SelectField(label='Cultivation Type', validators=[DataRequired()], choices=[('mono','Mono'), ('mix','Mix'), ('multi','Multi')])



# SET UP AGRIMODULE FORMS
class CultivationProcessForm(FlaskForm):
    cultivation_process     = SelectField(label='Cultivation Process', validators=[DataRequired()], choices=[('Organic','Organic'),('Chemical','Chemical')])

class CultivationTypeForm(FlaskForm):
    cultivation_type        = SelectField(label='Cultivation Type', validators=[DataRequired()], choices=[('mono','Mono'), ('mix','Mix'), ('multi','Multi')])

class CultivationStateForm(FlaskForm):
    cultivation_state       = SelectField(label='Cultivation State', validators=[DataRequired()], choices=[('new','New'),('Already Growing','Already Growing')])

class CultivationStartDateForm(FlaskForm):
    cultivation_start_date  = DateField(label='Cultivation Start Date', format='%Y-%m-%d', validators=[DataRequired()])

class CultivationCropForm(FlaskForm):
    cultivation_crop        = SelectField(label='Cultivation Crop', validators=[DataRequired()], choices=[('plum','Plum'),('romaine','Romaine'),('arugula','Arugula')], option_widget=None)

class CultivationAreaForm(FlaskForm):
    cultivation_area       = FloatField(label='Cultivation Area', validators=[DataRequired(), NumberRange(min=5, max=5000, message='Area between 5 and 5000 m2')])


class PreNewCropForm:
    def __init__(self, field_cultivation_area, field_cultivation_start_date, field_cultivation_state, field_cultivation_type):
        self.field_cultivation_area          = field_cultivation_area
        self.field_cultivation_start_date    = field_cultivation_start_date
        self.field_cultivation_state         = field_cultivation_state
        self.field_cultivation_type          = field_cultivation_type
class PreDateNewCropForm:
    def __init__(self, field_cultivation_start_date):
        self.field_cultivation_start_date = field_cultivation_start_date

class NewCropForm(FlaskForm):
    farm_choices                  = SelectField(label='Choose Farm', validators=[DataRequired()], coerce = int)
    field_cultivation_area        = FloatField(label='Field Cultivation Area', validators=[DataRequired()], render_kw={'placeholder':'Field area should not exceed the available land on your farm'})
    field_cultivation_crop        = SelectField(label='Cultivation Crop', validators=[DataRequired()], coerce = int)
    field_cultivation_start_date  = DateField(label='Cultivation Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    field_cultivation_state       = SelectField(label='Cultivation State', validators=[DataRequired()], choices=[('new','New'),('already growing','Already Growing')])
    field_cultivation_type        = SelectField(label='Cultivation Type', validators=[DataRequired()], choices=[('mono','Mono'), ('mix','Mix'), ('multi','Multi')])

class PreEditFarmForm:
    def __init__(self, farm_name, farm_location, farm_area, farm_cultivation_process):
        self.farm_name                  = farm_name
        self.farm_location              = farm_location
        self.farm_area                  = farm_area
        self.farm_cultivation_process   = farm_cultivation_process

class EditFarmForm(FlaskForm):
    farm_name                   = StringField('Farm name', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    farm_location               = StringField('Farm location', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    farm_area                   = FloatField('Farm Cultivation Area', validators=[DataRequired(), NumberRange(min=1, max=5000, message='Area between 1 and 5000 m2')])
    farm_cultivation_process    = SelectField('Farm Cultivation Process', validators=[DataRequired()], choices=[('Organic','Organic'),('Chemical','Chemical')])



# MANAGE SYSTEMS FORMS

class NewAgrimoduleForm(FlaskForm):
    name                = StringField('Agrimodule name', validators=[DataRequired(), Length(min=2, max=30, message='Give it a name for sanity MAX 30.')])
    identifier          = StringField('Agrimodule code', validators=[DataRequired(), Length(min=2, max=30, message='Your agrimodule identifier is in the back of your agrimodule.')])
    lat                 = FloatField('latitude location', validators=[DataRequired(), NumberRange(min=-90, max=90, message='write the lat coordinates')])
    lon                 = FloatField('longitude location', validators=[DataRequired(), NumberRange(min=-180, max=180, message='write the lon coordinates')])
    field_choices       = SelectField('Field to monitor:', validators=[Optional(strip_whitespace=True)], coerce = int)

# '/user/farm/field/agrimodule/add-sensor'
class AgrimoduleAddSensorForm(FlaskForm):
    agrimodule_choices  = SelectField(label='Agrimodule choices', validators=[DataRequired()], coerce = int)
    sensor_choices      = SelectField(label='Agrimodule choices', validators=[DataRequired()], choices=[('Agrisensor','Agrisensor'),('Agripump','Agripump')])
    identifier          = StringField('Sensor code', validators=[DataRequired(), Length(min=2, max=30, message='Your sensor system identifier is in the back of your device.')])

# '/user/farm/field/agrimodule/edit-agrimodule/<agrimodule_id>'
class PreEditAgrimoduleForm:
    def __init__(self, name, field_choices):
        self.name = name
        self.field_choices = field_choices

class EditAgrimoduleForm(FlaskForm):
    name                = StringField('Agrimodule name', validators=[DataRequired(), Length(min=2, max=30, message='Give it a name for sanity MAX 30.')])
    field_choices       = SelectField(label='Field to monitor:', validators=[Optional(strip_whitespace=True)], coerce = int)

# '/user/farm/field/agripump/change-pump/'
class PreEditAgripumpForm:
    def __init__(self, pump_choices):
        self.pump_choices = pump_choices

class EditAgripumpForm(FlaskForm):
    pump_choices        = SelectField(label='Pump choices', validators=[Optional(strip_whitespace=True)], coerce = int)





# FARM SETUP SYSTEM
class FarmInfoForm(FlaskForm):
    farm_name                    = StringField('Farm name', validators=[DataRequired(), Length(min=2, max=30, message='Your farm name needs to be at least 2 characters long.')])
    farm_location                = StringField('Farm location (city)',   validators=[DataRequired(), Length(max=30, message='Type the city name and it needs to be max 30 characters long.')])
    farm_area                    = FloatField('Farm area (meter square)', validators=[DataRequired(), NumberRange(min=5, max=5000, message='Area between 5 and 5000 m2')])
    farm_cultivation_process     = SelectField('Farm Cultivation Process', validators=[DataRequired()], choices=[('Organic','Organic'),('Chemical','Chemical')])


# FlaskFOrm constructor
class ContactUsForm:
    def __init__(self, name, email, phone, msg):
        self.name = name
        self.email = email
        self.phone = phone
        self.msg = msg
class ContactUsForm(FlaskForm):
    name    = StringField(label='Fullname', validators=[DataRequired(), Length(min=3, max=30, message=None)])
    email   = StringField('Email', validators=[DataRequired(), Length(min=5, max=30, message=None), Email()])
    phone   = StringField('Phone', validators=[DataRequired(), Length(min=7, max=30, message=None)])
    msg     = TextAreaField ('Message', validators=[DataRequired(), Length(min=-1, max=1000, message='Maximum characters: 1000')])

# field enclosures - can
class PhoneForm(Form):
    country_code = IntegerField(label='Country Code:')
    area_code = IntegerField(label='Area Code:')
    number = IntegerField(label='Number:')

class ContactUsFormEG(FlaskForm):
    name    = StringField(label='Fullname', validators=[DataRequired(), Length(min=3, max=30, message=None)])
    email   = StringField('Email', validators=[DataRequired(), Length(min=5, max=30, message=None), Email()])
    phone   = StringField('Phone', validators=[DataRequired(), Length(min=7, max=30, message=None)])
    msg     = TextAreaField ('Message', validators=[DataRequired(), Length(min=-1, max=1000, message='Maximum characters: 1000')])
    # Inherits from PhoneForm the fields that are there
    home_phone  = FormField(PhoneForm)
    handy_phone = FormField(PhoneForm)
    work_phone  = FormField(PhoneForm)


# ContactUsFormExtended inherits all fields from ContactUsForm
class ContactUsFormExtended(ContactUsFormEG):
    city    = StringField(label='City', validators=[DataRequired()])
    country = StringField(label='Country', validators=[DataRequired()])

class ContactUsFormExtendedOne(ContactUsFormEG):
    start_date = DateField(label='Start Date', format='%Y-%m-%d')
# SNIPETS
# default='Carlos' # an atribute that can be pass inside the Field() of FlaskForm
