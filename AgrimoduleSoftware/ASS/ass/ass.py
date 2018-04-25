from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

from datetime import datetime
from sqlalchemy.sql import func

# Create app
app = Flask(__name__)

app.config.from_pyfile('cfg.cfg')

# Create database connection object
db = SQLAlchemy(app)

# DEFINE USER MODELS FLASK-SECURITY
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime(timezone=True))
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    # RELATIONSHIP
    # USER[1]-FARM[M]
    farms = db.relationship('Farm', backref='user', lazy='dynamic')
    # USER[1]-AGRIMODULESMARTSYSTEM[M]
    agrimodule_smart_systems = db.relationship('AgrimoduleSmartSystem', backref='user', lazy='dynamic')
    # USER[1]-PUMP[M]
    pumps = db.relationship('Pump', backref='user', lazy='dynamic')

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<user {}>'.format(self.email)

# DEFINE FARMS AND AGRIMODULE MODELS
class Farm(db.Model):
    """Farms Models for Users to create. One User can created as many farms as he wants"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    location = db.Column(db.String(20))
    size = db.Column(db.Float(precision=2))

    # RELATIONSHIP
    # USER[1]-FARM[M]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # FARM[1]-FIELD[M]
    fields = db.relationship('Field', backref='farm', lazy='dynamic')

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<farm {}>'.format(self.name)

crops_field = db.Table('crops_field',
    db.Column('field_id', db.Integer, db.ForeignKey('field.id')),
    db.Column('crop_id', db.Integer, db.ForeignKey('crop.id'))
    )

class Field(db.Model):
    """Fields that can exist inside the Farm.Model. One Farm can have as many Fields within for different crops to be cultivated, being limited by the size of the Farm"""
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(25), nullable=False)
    size = db.Column(db.Float(precision=3))
    date_start = db.Column(db.DateTime(timezone=True))
    date_finish = db.Column(db.DateTime(timezone=True))
    _current_yield = db.Column(db.Float(precision=2))

    # RELATIONSHIP
    # FIELD[M]-CROP[M]
    crops = db.relationship('Crop', secondary='crops_field', backref='field', lazy='dynamic')
    # FARM[1]-FIELD[M]
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))
    
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<field {}>'.format(self.crop)

class Crop(db.Model):
    '''The crop database reference from farmers or Users.model that can be be cultivated in the Field.Model'''
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(25), unique=True, nullable=False)
    _variety = db.Column(db.String(25))
    _family = db.Column(db.String(25))
    _yield = db.Column(db.Float(precision=3))
    _space_x = db.Column(db.Float(precision=2))
    _space_y = db.Column(db.Float(precision=2))
    _density = db.Column(db.Float(precision=2))
    # FRUITS EACH PLANT
    _fruit_quantity = db.Column(db.Integer)
    _fruit_size = db.Column(db.Float(precision=2))
    _fruit_weight = db.Column(db.Float(precision=2))
    # RESOURCES REQUIRED
    _water = db.Column(db.Float(precision=4))
    _nutrient = db.Column(db.Float(precision=4))
    _radiation = db.Column(db.Float(precision=4))
    # CYCLE
    _cycle_dtg_days = db.Column(db.Integer)
    _cycle_dtm_days = db.Column(db.Integer)
    # REQUIREMENTS
    # SOIL
    _soil_ph_min = db.Column(db.Float(precision=2))
    _soil_ph_opt = db.Column(db.Float(precision=2))
    _soil_ph_max = db.Column(db.Float(precision=2))

    _soil_temp_min = db.Column(db.Float(precision=2))
    _soil_temp_opt = db.Column(db.Float(precision=2))
    _soil_temp_max = db.Column(db.Float(precision=2))

    _soil_humi_min = db.Column(db.Float(precision=2))
    _soil_humi_opt = db.Column(db.Float(precision=2))
    _soil_humi_max = db.Column(db.Float(precision=2))

    _soil_nutrient_min = db.Column(db.Float(precision=2))
    _soil_nutrient_opt = db.Column(db.Float(precision=2))
    _soil_nutrient_max = db.Column(db.Float(precision=2))
    # AIR
    _air_temp_min = db.Column(db.Float(precision=2))
    _air_temp_opt = db.Column(db.Float(precision=2))
    _air_temp_max = db.Column(db.Float(precision=2))

    _air_humi_min = db.Column(db.Float(precision=2))
    _air_humi_opt = db.Column(db.Float(precision=2))
    _air_humi_max = db.Column(db.Float(precision=2))

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<crop {}>'.format(self._name)

class AgrimoduleSmartSystem(db.Model):
    """Each agrimodule smart system is unique and has am agrimodule an agripump and maybe agresiensor and other agripumps depending on the complaexity of the farm
    and can be added to any user any farm with a unique identuifier which can connect the data being sent to server to an specific User.Model/Field.Model
    Each agrimodule"""
    id = db.Column(db.Integer, primary_key=True)
    _identifier_agrimodule = db.Column(db.String(50), unique=True, nullable=False)
    _identifier_agripump = db.Column(db.String(50), unique=True, nullable=False)
    # LOCATION
    _lat_agrimodule = db.Column(db.Float(precision=8), nullable=False)
    _lon_agrimodule = db.Column(db.Float(precision=8), nullable=False)
    _lat_agripump = db.Column(db.Float(precision=8))
    _lon_agripump = db.Column(db.Float(precision=8))

    # RELATIONSHIP
    # AGRIMODULESMARTSYSTEM[1]-AGRIMODULEMEASUREMENT[M]
    agrimodule_measurements = db.relationship('AgrimoduleMeasurement', backref='agrimodulesmartsystem', lazy='dynamic')
    # AGRIMODULESMARTSYSTEM[1]-AGRIPUMPSCHEDULE[M]
    agripump_schedules = db.relationship('AgripumpSchedule', backref='agrimodulesmartsystem', lazy='dynamic')
    # USER[1]-AGRIMODULESMARTSYSTEM[M]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<agrimodule {}>'.format(self.identifier)

class AgrimoduleMeasurement(db.Model):
    """each agrimodule has a different table where all data that is measured by agrimodule is saved in this model"""
    id = db.Column(db.Integer, primary_key=True)
    soil_ph = db.Column(db.Float(precision=4))
    soil_nutrient = db.Column(db.Float(precision=4))
    soil_temp = db.Column(db.Float(precision=4))
    soil_humi = db.Column(db.Float(precision=4))
    air_temp = db.Column(db.Float(precision=4))
    air_humi = db.Column(db.Float(precision=4))
    air_pres = db.Column(db.Float(precision=4))
    solar_radiation = db.Column(db.Float(precision=4))
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    
    # RELATIONSHIP
    # AGRIMODULESMARTSYSTEM[1]-AGRIMODULEMEASUREMENT[M]
    agrimodule_smart_system_id = db.Column(db.Integer, db.ForeignKey('agrimodulesmartsystem.id'))

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<agrimodulemeasurements {}>'.format(self.date)

class Pump(db.Model):
    """pump database used for each field or each agripump whichi is installed in the farm. one farm can ahve as many pump the want as long as the have an agripump for it"""
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(25))
    flow_rate = db.Column(db.Float(precision=2), nullable=False)
    height_max = db.Column(db.Float(presicion=2), nullable=False)
    kwh = db.Column(db.Float(precision=2), nullable=False)

    # RELATIONSHIP
    # USER[1]-PUMP[M]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # PUMP[1]-AGRIPUMPSCHEDULE
    agripump_schedules = db.relationship('Pump', backref='pump', lazy='dynamic')
    
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<pump {}>'.format(self.brand)   

class AgripumpSchedule(db.Model):
    """pump schedule for each farm and agripump, it requires to know which Pump.Model is used in order to make the calculations"""
    id = db.Column(db.Integer, primary_key=True)
    # REQUIREMENTS
    _daily_water = db.Column(db.Float(precision=3))
    _date = db.Column(db.DateTime(timezone=True), nullable=False)
    # SCHEDULE IN MINUTES
    _00_HOUR = db.Column(db.Float(precision=1))
    _01_HOUR = db.Column(db.Float(precision=1))
    _02_HOUR = db.Column(db.Float(precision=1))
    _03_HOUR = db.Column(db.Float(precision=1))
    _04_HOUR = db.Column(db.Float(precision=1))
    _05_HOUR = db.Column(db.Float(precision=1))
    _06_HOUR = db.Column(db.Float(precision=1))
    _07_HOUR = db.Column(db.Float(precision=1))
    _08_HOUR = db.Column(db.Float(precision=1))
    _09_HOUR = db.Column(db.Float(precision=1))
    _10_HOUR = db.Column(db.Float(precision=1))
    _11_HOUR = db.Column(db.Float(precision=1))
    _12_HOUR = db.Column(db.Float(precision=1))
    _13_HOUR = db.Column(db.Float(precision=1))
    _14_HOUR = db.Column(db.Float(precision=1))
    _15_HOUR = db.Column(db.Float(precision=1))
    _16_HOUR = db.Column(db.Float(precision=1))
    _17_HOUR = db.Column(db.Float(precision=1))
    _18_HOUR = db.Column(db.Float(precision=1))
    _19_HOUR = db.Column(db.Float(precision=1))
    _20_HOUR = db.Column(db.Float(precision=1))
    _21_HOUR = db.Column(db.Float(precision=1))
    _22_HOUR = db.Column(db.Float(precision=1))
    _23_HOUR = db.Column(db.Float(precision=1))

    # REALTIONSHIPS
    # AGRIMODULESMARTSYSTEM[1]-AGRIPUMPSCHEDULE[M]
    agrimodule_smart_system_id = db.Column(db.Integer, db.ForeignKey('agrimodulesmartsystem.id'))
    # PUMP[1]-AGRIPUMPSCHEDULE[M]
    pump_id = db.Column(db.Integer, db.ForeignKey('pump.id'))
    
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<pump {}>'.format(self.brand)   

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Views
@app.route('/')
# @login_required
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()