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

    def __repr__(self):
        return '<user {}>'.format(self.email)

# DEFINE FARMS AND AGRIMODULE MODELS
class Farm(db.Model):
    """Farms Models for Users to create. One User can created as many farms as he wants"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    location = db.Column(db.String(20))
    size = db.Column(db.Float(precision=2))
    
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return '<farm {}>'.format(self.name)

class Field(db.Model):
    """Fields that can exist inside the Farm.Model. One Farm can have as many Fields within for different crops to be cultivated, being limited by the size of the Farm"""
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(25), nullable=False)
    size = db.Column(db.Float(precision=3))
    date_start = db.Column(db.DateTime(timezone=True))
    date_finish = db.Column(db.DateTime(timezone=True))
    _current_yield = db.Column(db.Float(precision=2))
    
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

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
    _time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return '<crop {}>'.format(self._name)

class Agrimodule(db.Model):
    """Each agrimodule is unique and can be added to any user any farm with a unique identuifier which can connect the data being sent to server to an specific User.Model/Field.Model
    Each agrimodule"""
    id = db.Column(db.Integer, primary_key=True)
    _identifier = db.Column(db.String(50), unique=True, nullable=False)
    # LOCATION
    _lat = db.Column(db.Float(precision=8), nullable=False)
    _lon = db.Column(db.Float(precision=8), nullable=False)

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return '<agrimodule {}>'.format(self.identifier)

class AgrimoduleMeasurements(db.Model):
    """pump database used for each field or each agripump whichi is installed in the farm. one farm can ahve as many pump the want as long as the have an agripump for it"""
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
    
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return '<agrimodulemeasurements {}>'.format(self.date)


class Pump(db.Model):
    """pump database used for each field or each agripump whichi is installed in the farm. one farm can ahve as many pump the want as long as the have an agripump for it"""
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(25))
    flow_rate = db.Column(db.Float(precision=2), nullable=False)
    height_max = db.Column(db.Float(presicion=2), nullable=False)
    kwh = db.Column(db.Float(precision=2), nullable=False)
    # add overhead or pressure on height variable
    
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

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