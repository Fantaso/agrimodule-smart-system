from flask import Blueprint, render_template, redirect, url_for, flash, session
from solarvibes import db
from solarvibes.welcome.forms import FarmForm, FieldForm, AddAgrisysForm, InstallAgrisysForm, AddPumpForm
from solarvibes.models import Crop, Farm, Field, Pump, Agrimodule, Agrisensor, Agripump
from flask_login import current_user
from flask_security import login_required
from math import sqrt, floor

welcome = Blueprint(
    'welcome',
    __name__,
    template_folder="templates"
)

#############################
#############################
# WELCOME VIEWS
#############################
#############################

###################
# WELCOME
###################
# TODO: this should be check somewhere else. before it calls this blurprint
@welcome.route('/', methods=['GET'])
@login_required
def index():
    if current_user.agrimodules.count() == 0:
        flash('welcome for the first time, ' + current_user.name + '!')
        print('welcome for the first time, ' + current_user.name + '!')
        set_sys_flag = True
        return render_template('welcome/welcome.html', user=current_user, set_sys_flag=set_sys_flag)
    elif current_user.farms.count() == 0 or current_user.farms.first().fields.count() == 0:
        flash('Now set your farm, ' + current_user.name + '!')
        print('Now set your farm, ' + current_user.name + '!')
        set_sys_flag = False
        return render_template('welcome/welcome.html', user=current_user, set_sys_flag=set_sys_flag)
    else:
        default_farm = current_user.farms.filter_by(_default = 1).one()
        # return 'go to welcome blueprint and fix this return'
        return redirect(url_for('main.index', user=current_user, default_farm=default_farm))

###################
# SET FARM
###################
@welcome.route('/set-farm', methods=['GET', 'POST'])
@login_required
def welcome_set_farm():
    if 'set_farm' not in session:
        session['set_farm'] = dict()
        session.modified = True

    form = FarmForm()               # CREATE WTForm FORM
    if form.validate_on_submit():   # IF request.methiod == 'POST'
        def m2_to_cm2(m2):
            return m2 * 10000

        # USER OBJS
        user_id = current_user.get_id()

        # FARM OBJS
        farm_name = form.farm_name.data
        farm_location = form.farm_location.data
        farm_area = form.farm_area.data
        farm_cultivation_process = form.farm_cultivation_process.data
        print (form.farm_name.data)
        print (form.farm_location.data)
        print (form.farm_area.data)
        print (form.farm_cultivation_process.data)

        # FARM OBJS  TO DB
        farm = Farm(    user_id=user_id,
                        farm_name=farm_name,
                        farm_location=farm_location,
                        farm_area=m2_to_cm2(farm_area),
                        farm_cultivation_process=farm_cultivation_process,
                        _default=False)
        print(farm)

        # DB COMMANDS
        db.session.add(farm)
        db.session.commit()

        # OBJS SAVE ON SESSION
         # ADD SESSION OBJS
        farm_id = farm.id
        session['set_farm'].update({'user_id': user_id,
                                'farm_id':farm_id,
                                'farm_name':farm_name,
                                'farm_location':farm_location,
                                'farm_area':farm_area,
                                'farm_cultivation_process':farm_cultivation_process})
        session.modified = True
        print (session['set_farm'])

        # DEAFULT FARM
        if current_user.farms.count() == 1: # if first time and first farm, set it as the default one
            print('Farm default nummer {} was added and type {}'.format(farm_id, type(farm_id)))
            current_user.default_farm_id = farm_id
            farm._default = True
            db.session.commit()


        # SUCESS AND REDIRECT TO NEXT STEP
        flash('''You just created farm: {}
                    located: {}
                    with an area: {} m2
                    growing: {}ally'''.format(farm_name, farm_location, farm_area, farm_cultivation_process))
        return redirect(url_for('welcome.welcome_set_field'))

    return render_template('welcome/welcome_set_farm.html', form=form)


###################
# SET FIELD
###################
@welcome.route('/set-field', methods=['GET', 'POST'])
@login_required
def welcome_set_field():

    crop_choices = Crop.query.all()


    form = FieldForm()              # CREATE WTForm FORM
    form.field_cultivation_crop.choices = [ (crop.id,  str.capitalize(crop._name)) for crop in crop_choices ]
    form.field_cultivation_crop.choices.insert(0, ('0' ,'Choose:'))

    if form.validate_on_submit():   # IF request.methiod == 'POST'
        # USER OBJS
        user = User.query.filter_by(id = session['set_farm']['user_id']).first()
        farm = user.farms.filter_by(id = session['set_farm']['farm_id']).first()

        # FIELD OBJS
        print(form.field_cultivation_crop.data)
        print(Crop.query.filter_by(id = form.field_cultivation_crop.data).first())

        crop = Crop.query.filter_by(id = form.field_cultivation_crop.data).first()
        field_name = form.field_name.data
        field_cultivation_area = form.field_cultivation_area.data
        field_cultivation_start_date = form.field_cultivation_start_date.data
        field_cultivation_state = form.field_cultivation_state.data
        field_cultivation_type = form.field_cultivation_type.data



        def m2_to_cm2(m2):
            return m2 * 10000

        def num_plants():
            area_in_cm2 = m2_to_cm2(field_cultivation_area) # cm2
            distance_rows_and_columns = sqrt(area_in_cm2) # cm. since we receive an area instead of a shape, we assumed is perfect square
            num_of_rows = (floor(distance_rows_and_columns / crop._space_x))/2 #
            num_of_cols = (floor(distance_rows_and_columns / crop._space_y))/2 # since space of plant and space for walk is the same DIVIDE by 2
            num_of_plants = num_of_rows * num_of_cols
            return num_of_plants

        # Calculated vars
        field_cultivation_finish_date = field_cultivation_start_date + timedelta(crop._dtg + crop._dtm) # datetime
        field_num_plants = num_plants() # number Integer
        field_projected_yield = crop._yield * field_num_plants # gr
        field_current_yield = 0
        field_water_required_day = field_num_plants * crop._water

        print('''finish date: {}
                 num plants: {} #
                 project yield: {} gr
                 water per day {} ml'''.format(field_cultivation_finish_date, field_num_plants, field_projected_yield, field_water_required_day))


        # FIELD OBJS TO DB
        field = Field(  field_name=field_name,
                        farm=farm,
                        field_cultivation_area=m2_to_cm2(field_cultivation_area),
                        field_cultivation_start_date=field_cultivation_start_date,
                        field_cultivation_state=field_cultivation_state,
                        field_cultivation_type=field_cultivation_type,
                        field_cultivation_finish_date = field_cultivation_finish_date,
                        field_current_yield = field_current_yield,
                        field_num_plants = field_num_plants,
                        field_water_required_day = field_water_required_day,
                        field_projected_yield = field_projected_yield)
        field.crops.append(crop)

        # DB COMMANDS
        db.session.add(field)
        db.session.commit()

        # DEAFULT AGRIMODULE SYSTEM
        if current_user.farms.count() == 1 and current_user.farms.first().fields.count() == 1 and current_user.agrimodules.count() > 0: # if first time and first field, set it as the default one
            print('Field default agrimodule system nummer {} was added and type {}'.format(field.id, type(field.id)))
            field.agrimodule = Agrimodule.query.first()
            db.session.commit()

        #SUCESS AND REDIRECT TO DASHBOARD
        flash('You just created a {} in your {}'.format(field_name, farm.farm_name))
        del session['set_farm']     # ERASE SESSION OBJS
        return redirect(url_for('welcome.index'))

    return render_template('welcome/welcome_set_field.html', form=form)

    # field_cultivation_area = db.Column(db.Float(precision=2))
    # field_cultivation_start_date = db.Column(db.DateTime(timezone=True))
    # field_cultivation_finish_date = db.Column(db.DateTime(timezone=True))
    # field_current_yield = db.Column(db.Float(precision=2))
    # field_projected_yield = db.Column(db.Float(precision=2))
    # field_cultivation_state = db.Column(db.String(20))
    # field_cultivation_type = db.Column(db.String(5))

    # field_num_plants = db.Column(db.Integer)
    # field_spacing_topology = db.Column(db.String(20))
    # field_water_required_day = db.Column(db.Integer)


# def user_crop_status():
#     user = User.query.filter_by(id = current_user.get_id()).first()
#     farm = user.farms.first()
#     field = farm.fields.first()
#     print (field)
#     print (field.cultivation_area)
#     print (field.cultivation_start_date)
#     print (field.cultivation_finish_date)
#     print (field._current_yield)
#     crop = field.crops.first()
#     print (crop)
#     print (crop._variety)
#     print (crop._name)
#     num_of_plants = ( field.cultivation_area / crop._density )
#     cycle_days = ( crop._dtm + crop._dtg )
#     cycle_days_so_far = ( datetime.now() - field.cultivation_start_date ).days
#     print (num_of_plants)
#     print (cycle_days)
#     print (cycle_days_so_far)
#     calc_values = {'num_of_plants' : num_of_plants, 'cycle_days' : cycle_days, 'cycle_days_so_far' : cycle_days_so_far}
#     print (calc_values)
#     return render_template('welcome/user_crop_status.html', crop = crop, field = field, calc_values = calc_values)


##########################################################
##########################################################
# SET SYS
##########################################################
##########################################################
@welcome.route('/set-sys', methods=['GET'])
@login_required
def welcome_set_sys():
    return render_template('welcome/welcome_set_sys.html')


###################
# SET FARM INFO
###################
# @welcome.route('/set-sys/farm-info', methods=['GET', 'POST'])
# @login_required
# def farm_info():

#     if 'set_sys' not in session:
#         session['set_sys'] = dict()
#         session.modified = True

#     form = FarmInfoForm()
#     if form.validate_on_submit():
#         # USER OBJS
#         user_id = current_user.get_id()

#         # FARM INFO OBJS
#         farm_name = form.farm_name.data
#         farm_location = form.farm_location.data
#         farm_area = form.farm_area.data
#         farm_cultivation_process = form.farm_cultivation_process.data
#         print (form.farm_name.data)
#         print (form.farm_location.data)
#         print (form.farm_area.data)
#         print (form.farm_cultivation_process.data)

#         # OBJS TO DB
#         farm = Farm(user_id=user_id,
#                     farm_name=farm_name,
#                     farm_location=farm_location,
#                     farm_area=farm_area,
#                     farm_cultivation_process=farm_cultivation_process)
#         print(farm)

#         # DB COMMANDS
#         db.session.add(farm)
#         db.session.commit()

#         # ADD SESSION OBJS
#         farm_id = farm.id
#         print(farm_id)
#         session['set_sys'].update({'user_id': user_id,
#                                 'farm_id':farm_id,
#                                 'farm_name':farm_name,
#                                 'farm_location':farm_location,
#                                 'farm_area':farm_area,
#                                 'farm_cultivation_process':farm_cultivation_process})
#         session.modified = True
#         print (session['set_sys'])


#         # FLASH AND REDIRECT
#         flash('''You just created farm: {}
#                     located: {}
#                     with an area: {} m2
#                     growing: {}ally'''.format(farm_name, farm_location, farm_area, farm_cultivation_process))
#         return redirect(url_for('welcome.add_agrisys'))

#     return render_template('welcome/farm_info.html', form=form)

###################
# SET CONNECT ASS
###################
@welcome.route('/set-sys/add-agrisys', methods=['GET', 'POST'])
@login_required
def add_agrisys():

    if 'set_sys' not in session:
        session['set_sys'] = dict()
        session.modified = True

    form = AddAgrisysForm()
    if form.validate_on_submit():
        # USER OBJS
        user = current_user

        # ADD AGRISYS OBJS
        agrimodule_name = form.agrimodule_name.data
        agrimodule_identifier = form.agrimodule_identifier.data


        # OBJS TO DB
        agrimodule = Agrimodule(name = agrimodule_name, identifier = agrimodule_identifier, user = user)


        # DB COMMANDS
        db.session.add(agrimodule)
        db.session.commit()

        # ADD SESSION OBJS
        session['set_sys'].update({'agrimodule_identifier':agrimodule_identifier, 'agrimodule_id':agrimodule.id})
        session.modified = True


        # FLASH AND REDIRECT
        flash('Your agrimodule identifier is: {}'.format(agrimodule_identifier))
        return redirect(url_for('welcome.install_agrisys'))
    return render_template('welcome/add_agrisys.html', form=form)



###################
# SET INSTALL ASS
###################
@welcome.route('/set-sys/install-agrisys', methods=['GET', 'POST'])
@login_required
def install_agrisys():
    form = InstallAgrisysForm()
    if form.validate_on_submit():
        # USER OBJS
        user = current_user

        # INSTALL AGRISYS OBJS
        agm_lat = form.agm_lat.data
        agm_lon = form.agm_lon.data
        ags_lat = form.ags_lat.data
        ags_lon = form.ags_lon.data
        agp_lat = form.agp_lat.data
        agp_lon = form.agp_lon.data
        print (form.agm_lat)
        print (form.agm_lon)
        print (form.ags_lat)
        print (form.ags_lon)
        print (form.agp_lat)
        print (form.agp_lon)

        # OBJS TO DB
        agrimodule_id = session['set_sys']['agrimodule_id']
        agrisensor  = Agrisensor(agrimodule_id = agrimodule_id, lat = ags_lat, lon = ags_lon)
        agripump    =   Agripump(agrimodule_id = agrimodule_id, lat = agp_lat, lon = agp_lon)
        agrimodule = Agrimodule.query.filter_by(id = agrimodule_id).first()
        agrimodule.lat = agm_lat
        agrimodule.lon = agm_lon
        print(agrimodule_id)
        print(agrisensor)
        print(agripump)

        # DB COMMANDS
        db.session.add(agrisensor)
        db.session.add(agripump)
        db.session.commit()

        # ADD SESSION OBJS
        session['set_sys'].update({'agrimodule_id':agrimodule.id, 'agrisensor_id':agrisensor.id, 'agripump_id':agripump.id, 'agm_lat':agm_lat, 'agm_lon':agm_lon, 'ags_lat':ags_lat, 'ags_lon':ags_lon, 'agp_lat':agp_lat, 'agp_lon':agp_lon})
        session.modified = True
        print (session['set_sys'])



        # FLASH AND REDIRECT
        flash('''Your Agrimodule location is: LAT: {} LON: {}
                Your Agrisensor location is: LAT: {} LON: {}
                Your Agripump location is: LAT: {} LON: {}'''.format(agm_lat, agm_lon, ags_lat, ags_lon, agp_lat, agp_lon))
        return redirect(url_for('welcome.add_pump'))
    return render_template('welcome/install_agrisys.html', form=form)

###################
# SET ADD PUMP
###################
@welcome.route('/set-sys/add-pump', methods=['GET', 'POST'])
@login_required
def add_pump():

    form = AddPumpForm()
    if form.validate_on_submit():
        # USER OBJS
        user = current_user
        agrimodule = user.agrimodules.filter_by(id = session['set_sys']['agrimodule_id']).first()
        print(agrimodule)
        agripump = agrimodule.agripumps.filter_by(id = session['set_sys']['agripump_id']).first()
        print(agripump)

        def lps_to_mlpm(lps):
            return lps * (1000 * 60)
        def m_to_cm(m):
            return m * 100
        def kw_to_w(kw):
            return kw * 1000
        # ADD PUMP OBJS
        pump_name = form.pump_name.data
        pump_brand = form.pump_brand.data
        pump_flow_rate = lps_to_mlpm(form.pump_flow_rate.data)
        pump_head = m_to_cm(form.pump_head.data)
        pump_watts = kw_to_w(form.pump_watts.data)
        print(pump_brand)
        print(pump_flow_rate)
        print(pump_head)
        print(pump_watts)

        # OBJS TO DB
        pump = Pump(user = user, pump_name = pump_name, pump_brand = pump_brand, pump_flow_rate = pump_flow_rate, pump_head = pump_head, pump_watts = pump_watts)

        # DB COMMANDS
        db.session.add(pump)
        db.session.commit()

        # ADD PUMP TO AGRIPUMP
        agripump.pump_id = pump.id
        print(agripump.pump_id)
        db.session.commit()


        # OBJS SAVE ON SESSION
        session['set_sys'].update({'pump_id':pump.id, 'pump_brand':form.pump_brand.data, 'pump_flow_rate':form.pump_flow_rate.data, 'pump_head':form.pump_head.data, 'pump_watts':form.pump_watts.data})
        session.modified = True
        print (session['set_sys'])


        # FLASH AND REDIRECT
        flash('''Your Pump brand: {}
                Flow rate: {} lps
                Head pressure: {} m
                Wattage: {} kW'''.format(form.pump_brand, form.pump_flow_rate.data, form.pump_head.data, form.pump_watts.data))
        del session['set_sys']
        return redirect(url_for('welcome.welcome_set_farm'))
        # TODO: after welcome is complete need to go home.index

    return render_template('welcome/add_pump.html', form=form)
