from flask import render_template, session, request, redirect, url_for, flash, jsonify

from solarvibes import app, db

from flask_uploads import UploadSet, configure_uploads, IMAGES

from datetime import datetime, timedelta
from math import sqrt, floor

from flask_login import current_user

from flask_security import login_required

from solarvibes.models import roles_users, Role, User, Farm, Field, DailyFieldInput, Crop, Pump, Agrimodule, Agrisensor, Measurement, Agripump



#############################
#############################
# BEFORE REQUEST
#############################
#############################

@app.before_request
def before_request():
    ############ TESTS
    if current_user.is_anonymous:
    #         flash("hi is_anonymous")
            print("Hi is_anonymous")
    if current_user.is_authenticated:
    #         flash("hi "+str(g.user.id))
    #         print("hi "+str(g.user.id))
    #         flash("hi "+g.user.name)
            print("Hi "+current_user.name)
    # print( current_user )                     # PRINTS >  <user carlos@solar-vibes.com>
    # print( g.user )                           # PRINTS >  <user carlos@solar-vibes.com>
    # print( str( g.user.id ) )                 # PRINTS >  1
    # print( current_user.get_id() )            # PRINTS >  1
    # print(current_user.name)                  # PRINTS >  Carlos
    # print(g.user.name)                        # PRINTS >  Carlos
    # print(current_user.is_authenticated)      # PRINTS >  True
    # print(current_user.is_anonymous)          # PRINTS >  False

    # prt_obj(g.user)
    # print(g.user.name)

# if request.method == 'GET':
#         if current_user.is_authenticated:
#             uid = current_user.get_id()
#             name = User.query.filter_by(id=uid).first().name
#             return redirect(url_for('user', name=name, id=uid))
#         if current_user.is_anonymous:
#             flash("You can't view that farm without logging in :)")
#             return redirect(url_for('login'))
#         else:
#             flash("Log in, first :)")
#             return redirect(url_for('login'))





#############################
#############################
# APP VIEWS
#############################
#############################

# /user/    farm                            > main.index.html
# /user/    farm/  field                    >
# /user/    farm/  field/  agrimodule       > user_agrimodule.html
# /user/    farm/  field/  agripump         > user_agrimpump.html
# /user/    farm/  field/  crop-status      > user_crop_status.html

# /user/    welcome                         > welcome.html
# /user/    welcome/   set-farm             > welcome_set_farm.html
# /user/    welcome/   set-field            > welcome_set_field.html
# /user/    welcome/   set-sys              > welcome_set_sys.html

#############################
#############################
# INIT VIEW
#############################
#############################

# @app.route('/<name>/<farm-name>', methods=['GET', 'POST'])
# @login_required
# def farm(farm_name):
#     return 'you are in farm-name'

#############################
#############################
# WELCOME VIEW
#############################
#############################

# @app.route('/<name>/welcome', methods=['GET', 'POST'])
# @login_required
# def welcome(name):
#     return 'welcome' + str(name)

# @app.route('/<name>/welcome/set-farm', methods=['GET', 'POST'])
# @login_required
# def welcome_set_farm(name):
#     return 'set farm' + str(name)

# @app.route('/<name>/welcome/set-sys', methods=['GET', 'POST'])
# @login_required
# def welcome_set_sys(name):
#     return 'set sys' + str(name)

# @app.route('/<name>/welcome/sucess', methods=['GET', 'POST'])
# @login_required
# def welcome_sucess(name):
#     return 'set sys' + str(name)

#############################
#############################
# OLD VIEW
#############################
#############################

@app.route('/dashboard', methods=['GET'])
# @login_required
def dashboard():
    if request.method == 'GET':
        if current_user.is_authenticated:
            id = current_user.id
            name = User.query.filter_by(id=id).first().name
            return redirect(url_for('welcome'))
        if current_user.is_anonymous:
            flash("You can't view that farm without logging in :)")
            return redirect(url_for('login'))
        else:
            flash("Log in, first :)")
            return redirect(url_for('login'))

# /user/    farm                            > main.index.html
# /user/    farm/  field                    >
# /user/    farm/  field/  agrimodule       > user-agrimodule.html
# /user/    farm/  field/  agripump         > user-agrimpump.html
# /user/    farm/  field/  crop-status      > user-crop-status.html

# /user/    welcome                         > welcome.html
# /user/    welcome/   set-farm             > welcome-set-farm.html
# /user/    welcome/   set-field            > welcome-set-field.html
# /user/    welcome/   set-sys              > welcome-set-sys.html




##########################################################
##########################################################
# FARM VIEWS
##########################################################
##########################################################



##################
# USER AGRIMODULE
##################
@app.route('/user/farm/field/agrimodule', methods=['GET'])
@login_required
def user_agrimodule():
    user = User.query.filter_by(id = current_user.get_id()).first()
    farm = user.farms.first()
    field = farm.fields.first()
    crop = field.crops.first()
    print (crop)
    print (crop._soil_ph_min)
    print (crop._soil_ph_max)
    print (crop._soil_temp_min)
    print (crop._soil_temp_max)
    print (crop._soil_humi_min)
    print (crop._soil_humi_max)
    print (crop._soil_nutrient_min)
    print (crop._soil_nutrient_max)
    print (crop._air_temp_min)
    print (crop._air_temp_max)
    print (crop._air_humi_min)
    print (crop._air_humi_max)

    ag_measure = Agrimodule.query.first()
    print (ag_measure)
    print (ag_measure.soil_ph)
    print (ag_measure.soil_nutrient)
    print (ag_measure.soil_temp)
    print (ag_measure.soil_humi)
    print (ag_measure.air_temp)
    print (ag_measure.air_humi)
    print (ag_measure.air_pres)
    print (ag_measure.solar_radiation)
    print (ag_measure.batt_status)

    return render_template('user_agrimodule.html', ag_measure = ag_measure, crop = crop)

##################
# USER AGRIPUMP
##################
@app.route('/user/farm/field/agripump/', methods=['GET'])
@login_required
def user_agripump():

    user = User.query.filter_by(id = current_user.get_id()).first()
    farm = user.farms.first()
    field = farm.fields.first()
    crop = field.crops.first()
    agripump = Agripump.query.first()
    pump = user.pumps.filter_by(id = agripump.pump_id).first()
    print(user)
    print(farm)
    print(crop)
    print(pump)
    print(agripump)

    # calculating pump information
    def mlpm_to_lps(mlpm):
        return mlpm / (1000 * 60)
    def cm_to_m(cm):
        return cm / 100
    def w_to_kw(w):
        return w / 1000
    pump_info = {'pump_brand': pump.pump_brand, 'pump_flow_rate':mlpm_to_lps(pump.pump_flow_rate), 'pump_watts':w_to_kw(pump.pump_watts), 'pump_head':cm_to_m(pump.pump_head)}

    # Calculating energy consumption full cycle
    def w_to_wm(w):
        return w * 60
    def wm_to_kwh(wm):
        return wm / (60 * 60 * 1000)

    pump_Wmin_consumption = w_to_wm(pump.pump_watts)
    pump_minutes_on = field.field_water_required_day / pump.pump_flow_rate
    pump_Wmin_conmsumption_on = pump_Wmin_consumption * pump_minutes_on

    pump_consumption_kwh_per_day = wm_to_kwh(pump_Wmin_conmsumption_on)


    # AGRIPUMP
    # TIME USAGE
    # start_hour_per_day = db.Column(db.Integer)
    # qty_hour_per_day = db.Column(db.Integer)

    # time_per_hour = db.Column(db.Float)
    # time_per_day = db.Column(db.Float)
    # time_per_cycle = db.Column(db.Float)
    # WATER USAGE
    # water_per_hour = db.Column(db.Integer)
    # water_per_day = db.Column(db.Integer)
    # water_per_cycle = db.Column(db.Integer)
    # ENERGY USAGE
    # energy_per_hour = db.Column(db.Integer)
    # energy_per_day = db.Column(db.Integer)
    # energy_per_cycle = db.Column(db.Integer)

    # PUMP
    # brand = db.Column(db.String(25))
    # flow_rate = db.Column(db.Float(precision=2), nullable=False)
    # height_max = db.Column(db.Float(presicion=2), nullable=False)
    # wh = db.Column(db.Float(precision=2), nullable=False)


    return render_template('user_agripump.html', pump = pump_info, agripump = agripump, field = field, crop = crop, pump_consumption_kwh_per_day=pump_consumption_kwh_per_day)

##################
# USER CROP STATUS
##################
@app.route('/user/farm/field/crop-status', methods=['GET'])
@login_required
def user_crop_status():

    user = User.query.filter_by(id = current_user.get_id()).first()
    farm = user.farms.first()
    field = farm.fields.first()
    crop = field.crops.first()

    cycle_days_so_far = ( datetime.now() - field.field_cultivation_start_date ).days

    return render_template('user_crop_status.html', crop = crop, field = field, cycle_days_so_far = cycle_days_so_far)







##################
# USER WEATHER
##################
@app.route('/user/farm/weather', methods=['GET'])
@login_required
def user_weather():
    return render_template('user_weather.html')

##################
# USER ALERTS
##################
@app.route('/user/farm/alerts', methods=['GET', 'POST'])
@login_required
def user_alerts():
    return render_template('user_alerts.html')


##########################################################
##########################################################
# FARMER VIEWS
##########################################################
##########################################################

##################
# ALERTS
##################
@app.route('/user/farm/farmer/crop-planning', methods=['GET'])
@login_required
def user_crop_planning():
    return render_template('user_crop_planning.html')

##################
# CROP ANALYZER
##################
@app.route('/user/farm/farmer/crop-analyzer', methods=['GET'])
@login_required
def user_crop_analyzer():
    return render_template('user_crop_analyzer.html')

##################
# HEALTH ANALYZER
##################
@app.route('/user/farm/farmer/health-analyzer', methods=['GET'])
@login_required
def user_health_analyzer():
    return render_template('user_health_analyzer.html')

##################
# RESOURCES
##################
@app.route('/user/farm/farmer/resources', methods=['GET'])
@login_required
def user_resources():
    return render_template('user_resources.html')


##########################################################
##########################################################
# MARKET VIEWS
##########################################################
##########################################################

@app.route('/user/market', methods=['GET'])
@login_required
def user_market():
    return render_template('user_market.html')
