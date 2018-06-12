from flask import render_template, session, request, redirect, url_for, flash, jsonify

from solarvibes import app, db

from solarvibes.forms import EmailForm, EmailAndTextForm, ContactUsForm # Wesite Forms and users
from solarvibes.forms import RegisterFormExt, UserProfileForm, PreUserProfileForm # User Forms
from solarvibes.forms import FarmForm, FieldForm # Welcome Forms
from solarvibes.forms import FarmInfoForm, AddAgrisysForm, InstallAgrisysForm, AddPumpForm # Set-up System Forms
from solarvibes.forms import NewCropForm, PreDateNewCropForm, PreNewCropForm, EditFarmForm, PreEditFarmForm # Manage Farms Forms
from solarvibes.forms import AgrimoduleAddSensorForm, PreEditAgrimoduleForm, EditAgrimoduleForm, EditAgripumpForm, PreEditAgripumpForm, NewAgrimoduleForm # Manage Systems Forms
from solarvibes.forms import PreAddPumpForm # Manage Pumps Forms
from flask_uploads import UploadSet, configure_uploads, IMAGES

from datetime import datetime, timedelta
from math import sqrt, floor

from flask_login import current_user

from flask_security import login_required

from solarvibes.models import NewsletterTable, AgrimoduleFBTable, PlatformFBTable, WorkWithUsTable, ContactUsTable, roles_users, Role, User, Farm, Field, DailyFieldInput, Crop, Pump, Agrimodule, Agrisensor, Measurement, Agripump



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
# WEBSITE VIEWS
#############################
#############################

@app.route('/', methods=['GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('security.login'))
    return redirect(url_for('home'))
    # return redirect(url_for('login'))


@app.route('/indexweb', methods=('GET', 'POST'))
def indexweb():
    form = EmailForm()
    if form.validate_on_submit():
        email = form.email.data
        agrimodulefb = NewsletterTable(email=email)
        db.session.add(agrimodulefb)
        db.session.commit()
        form = None
        flash('Thanks. We will maintain you update!')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.route('/agrimodule', methods=('GET', 'POST'))
def agrimodule():
    form = EmailAndTextForm()
    if form.validate_on_submit():
        email = form.email.data
        msg = form.msg.data
        agrimodulefb = AgrimoduleFBTable(email=email, msg=msg)
        db.session.add(agrimodulefb)
        db.session.commit()
        form = None
        flash('Thanks. We definitely give a lot og thought about it!')
        return redirect(url_for('agrimodule'))
    return render_template('agrimodule.html', form=form)


@app.route('/platform', methods=('GET', 'POST'))
def platform():
    form = EmailAndTextForm()
    if form.validate_on_submit():
        email = form.email.data
        msg = form.msg.data
        platformfb = PlatformFBTable(email=email, msg=msg)
        db.session.add(platformfb)
        db.session.commit()
        form = None
        flash('Thanks. Your feedback is valuable to us!')
        return redirect(url_for('platform'))
    return render_template('platform.html', form=form)

@app.route('/about', methods=('GET', 'POST'))
def about():
    form = EmailAndTextForm()
    if form.validate_on_submit():
        email = form.email.data
        msg = form.msg.data
        workwithusus = WorkWithUsTable(email=email, msg=msg)
        db.session.add(workwithusus)
        db.session.commit()
        form = None
        flash('Thanks. Our HR department will contact you!')
        return redirect(url_for('about'))
    return render_template('about.html', form=form)


@app.route('/contact', methods=('GET', 'POST'))
def contact():
    # pre_contact = PreContactUsForm('Carlos','carlos@sv.de','+176-55858585','I would like to get a quotation for my farm 1 hectare located in Berlin')
    form = ContactUsForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        msg = form.msg.data
        newsletter = ContactUsTable(name=name, email=email, phone=phone, msg=msg)
        db.session.add(newsletter)
        db.session.commit()
        form = None
        flash('Thanks. We will get back to your shortly!')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)


#############################
#############################
# APP VIEWS
#############################
#############################

# /user/    farm                            > home.html
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

# /user/    farm                            > home.html
# /user/    farm/  field                    >
# /user/    farm/  field/  agrimodule       > user-agrimodule.html
# /user/    farm/  field/  agripump         > user-agrimpump.html
# /user/    farm/  field/  crop-status      > user-crop-status.html

# /user/    welcome                         > welcome.html
# /user/    welcome/   set-farm             > welcome-set-farm.html
# /user/    welcome/   set-field            > welcome-set-field.html
# /user/    welcome/   set-sys              > welcome-set-sys.html

#############################
#############################
# WELCOME VIEWS
#############################
#############################

###################
# WELCOME
###################
@app.route('/user/welcome', methods=['GET'])
@login_required
def welcome():
    if current_user.agrimodules.count() == 0:
        flash('welcome for the first time, ' + current_user.name + '!')
        print('welcome for the first time, ' + current_user.name + '!')
        set_sys_flag = True
        return render_template('welcome.html', user=current_user, set_sys_flag=set_sys_flag)
    elif current_user.farms.count() == 0 or current_user.farms.first().fields.count() == 0:
        flash('Now set your farm, ' + current_user.name + '!')
        print('Now set your farm, ' + current_user.name + '!')
        set_sys_flag = False
        return render_template('welcome.html', user=current_user, set_sys_flag=set_sys_flag)
    else:
        default_farm = current_user.farms.filter_by(_default = 1).one()
        return redirect(url_for('home', user=current_user, default_farm=default_farm))
    # if request.method == 'POST':

    # autenticar si el nombre de usuario q paso en el route es el mismo q esta autenticado
        # si no es el mismo. no puede ver la granja "esa no es tu granja. no la puedes ver.. mandar a su granja."
        # si si =  ver su gran. despues de preguntar si es su primera vez en app?
        # si si = mandarla a welcome new user page /user/welcome. instalacion de agri y detalles de granja
        # si no = mandarlo a /user/mainfarmname para que vea su granja normalmemnte.
    # if  g.user.id != current_user.id:
    #     flash('esa no es tu granja. no la puedes ver.. mandar a su granja.')
    #     print('esa no es tu granja. no la puedes ver.. mandar a su granja.')
    #     return redirect(url_for('login'))

    # elif g.user.farms.count() > 0:
    #     flash('welcome back ' + g.user.name)
    #     print('welcome back ' + g.user.name)
    #     return 'welcome back ' + g.user.name
        # return render_template('farm_home.html', name=g.user.name, last_name=g.user.last_name, email=g.user.email)
    # if current_user.farms.count() == 0:
    #     flash('welcome for the first time ' + current_user.name + '!')
    #     print('welcome for the first time ' + current_user.name + '!')
    #     # return g.user.name
    #     return redirect(url_for('welcome'))
    # else:
    #     return redirect(url_for('home'))

###################
# SET FARM
###################
@app.route('/user/welcome/set-farm', methods=['GET', 'POST']) # AQUI ME QUEDE
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
        return redirect(url_for('welcome_set_field'))

    return render_template('welcome_set_farm.html', form=form)


###################
# SET FIELD
###################
@app.route('/user/welcome/set-field', methods=('GET', 'POST'))
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
        return redirect(url_for('welcome'))

    return render_template('welcome_set_field.html', form=form)

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
#     return render_template('user_crop_status.html', crop = crop, field = field, calc_values = calc_values)


##########################################################
##########################################################
# SET SYS
##########################################################
##########################################################
@app.route('/user/welcome/set-sys', methods=['GET'])
@login_required
def welcome_set_sys():
    return render_template('welcome_set_sys.html')


###################
# SET FARM INFO
###################
# @app.route('/user/welcome/set-sys/farm-info', methods=['GET', 'POST'])
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
#         return redirect(url_for('add_agrisys'))

#     return render_template('farm_info.html', form=form)

###################
# SET CONNECT ASS
###################
@app.route('/user/welcome/set-sys/add-agrisys', methods=['GET', 'POST'])
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
        return redirect(url_for('install_agrisys'))
    return render_template('add_agrisys.html', form=form)



###################
# SET INSTALL ASS
###################
@app.route('/user/welcome/set-sys/install-agrisys', methods=['GET', 'POST'])
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
        return redirect(url_for('add_pump'))
    return render_template('install_agrisys.html', form=form)

###################
# SET ADD PUMP
###################
@app.route('/user/welcome/set-sys/add-pump', methods=['GET', 'POST'])
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
        return redirect(url_for('welcome'))

    return render_template('add_pump.html', form=form)

##########################################################
##########################################################
# HOME VIEW
##########################################################
##########################################################

@app.route('/user/farm', methods=('GET', 'POST'))
@login_required
def home():

    # default_farm = Farm.query.filter_by(id = user.default_farm_id).first()

    if current_user.agrimodules.count() == 0:
        flash('welcome for the first time ' + current_user.name + '!')
        print('welcome for the first time, ' + current_user.name + '!')
        set_sys_flag = True
        return render_template('welcome.html', current_user=current_user, set_sys_flag=set_sys_flag)
    elif current_user.farms.count() == 0 or current_user.farms.first().fields.count() == 0:
        flash('Now set your farm, ' + current_user.name + '!')
        print('Now set your farm, ' + current_user.name + '!')
        set_sys_flag = False
        return render_template('welcome.html', current_user=current_user, set_sys_flag=set_sys_flag)
    else:

        default_farm = current_user.farms.filter_by(_default = 1).one()
        fields = Field.query.filter_by(farm_id = default_farm.id).all()
        pump_db = Pump.query


        return render_template('home.html', user=current_user, default_farm = default_farm, fields = fields, pump_db =pump_db, timenow=datetime.now())


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
# USER FARMS
##################
@app.route('/user/farm/myfarms', methods=['GET'])
@login_required
def user_farms():

    # USER FARMS
    user = current_user
    farms = user.farms.all()

    def progress():
        for farm in farms:
            # print(farm)
            for field in farm.fields.all():
                # print(field)
                for crop in field.crops.all():
                    # print(crop)
                    cycle_days_so_far = ( datetime.now() - field.field_cultivation_start_date ).days
                    cycle_days = crop._dtm + crop._dtg
                    progress = (cycle_days_so_far / cycle_days) * 100
                    # print (cycle_days_so_far, cycle_days, progress)

    progress()
    timenow = datetime.now()





    # USER AGRIMODULES
    user = current_user
    agrimodules = user.agrimodules.all()

    # def list_agrimodules():
        # for agrimodule in agrimodules:
            # print(agrimodule, agrimodule.identifier)
            # for agripump in agrimodule.agripumps.all():
                # print(agripump, agripump.identifier)
            # for agrisensor in agrimodule.agrisensors.all():
                # print(agrisensor, agrisensor.identifier)

    # list_agrimodules()
    # USER PUMPS
    pumps = user.pumps.all()

    farm_db = Farm.query
    field_db = Field.query
    pump_db = Pump.query
    agripump_db = Agripump.query

    return render_template('user_farms.html', farms = farms, timenow = timenow, agrimodules=agrimodules, farm_db = farm_db, field_db = field_db, pump_db = pump_db, pumps=pumps, agripump_db = agripump_db)

##################
# USER MAKE FARM DEFAULT
##################
@app.route('/user/myfarms/default', methods=['GET'])
@app.route('/user/myfarms/default/<farm_id>', methods=['GET'])
@login_required
def user_farm_default(farm_id = None):

    if farm_id == None:
        flash('This page does not exist', _anchor = 'flash_msg')
        return redirect(url_for('user_farms'))

    # GET CURRENT DEFAULT FARM'S ID
    farm_default_old = current_user.farms.filter_by(_default = 1).one()
    farm_default_old._default = False # ERASE THE DEFAULT LABEL
    # GET NEW DEFAULT FARM
    farm_default_new = current_user.farms.filter_by(id = farm_id).one()
    farm_default_new._default = True # ADD THE DEFAULT LABEL
    current_user.default_farm_id = farm_id # COPY FARM DEFAULT ID TO USER'S TABLE
    db.session.commit()

    flash('New default farm: {}'.format(farm_default_new.farm_name))
    return redirect(url_for('user_farms'))


##################
# USER FIELD
##################
# @app.route('/user/farm/field', methods=['GET'])
# @login_required
# def user_field():
#     return render_template('field.html')

##################
# USER NEW FARM
##################
@app.route('/user/farm/new-farm', methods=['GET', 'POST'])
@login_required
def user_new_farm():

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

        # FARM OBJS  TO DB
        farm = Farm(    user_id=user_id,
                        farm_name=farm_name,
                        farm_location=farm_location,
                        farm_area=m2_to_cm2(farm_area),
                        farm_cultivation_process=farm_cultivation_process,
                        _default=False)

        # DB COMMANDS
        db.session.add(farm)
        db.session.commit()

        # SUCESS AND REDIRECT TO NEXT STEP
        flash('''You just created farm: {}
                    located: {}
                    with an area: {} m2
                    growing: {}ally'''.format(farm_name, farm_location, farm_area, farm_cultivation_process))
        return redirect(url_for('user_farms'))

    return render_template('user_new_farm.html', form=form)


##################
# USER EDIT FARM
##################
@app.route('/user/farm/edit-farm/<farm_id>', methods=['GET', 'POST'])
@login_required
def user_edit_farm(farm_id = 0):

    try:



        # None should pass to this route without the farm ID
        if farm_id == 0:
            return redirect(url_for('home'))

        # INTERNAL METHODS
        def cm2_to_m2(cm2):
            return cm2 / 10000

        def m2_to_cm2(m2):
            return m2 * 10000


        farm = Farm.query.filter_by(id = farm_id).first()

        myFarm = PreEditFarmForm(   farm_name = farm.farm_name,
                                    farm_location = farm.farm_location,
                                    farm_area = cm2_to_m2(farm.farm_area),
                                    farm_cultivation_process = farm.farm_cultivation_process)


        form = EditFarmForm(obj=myFarm)
        if form.validate_on_submit():

            # VALIDATE FIELD AREA
            def validate_area():
                farm_area = m2_to_cm2(form.farm_area.data) # in cm2
                fields_in_farm = farm.fields.all()
                sum_areas = 0

                for each_field in fields_in_farm:
                    sum_areas += each_field.field_cultivation_area # in cm2
                result = farm_area - sum_areas

                if result < 0:
                    return False
                return True

            if not validate_area():
                flash('Your new farm area should not be smaller than the total land of all your fields in: {}'.format(farm.farm_name))
                return render_template('user_edit_farm.html', form=form, farm_id = farm.id)


            # SAVING FORM DATA IN SESSION OBJ
            farm.farm_name = form.farm_name.data
            farm.farm_location = form.farm_location.data
            farm.farm_area = m2_to_cm2(form.farm_area.data)
            farm.farm_cultivation_process = form.farm_cultivation_process.data

            # DB COMMANDS
            db.session.commit()

            flash('You just edited your farm: {}'.format(farm.farm_name))
            return redirect(url_for('user_farms'))


        return render_template('user_edit_farm.html', form=form, farm_id = farm_id)





    except Exception as e:
        flash('that farm doesnt exist' + str(e))







##################
# USER DELETE FARM
##################
@app.route('/user/farm/delete-farm/<farm_id>', methods=['GET'])
@login_required
def user_delete_farm(farm_id):

    try:
        farm_to_del = Farm.query.filter_by(id = farm_id).first()
        fields_to_del_in_farm = farm_to_del.fields.all()
        for field in fields_to_del_in_farm:
            db.session.delete(field)
        db.session.delete(farm_to_del)
        db.session.commit()
        flash('You just deleted the farm: {}'.format(farm_to_del.farm_name))
        return redirect(url_for('user_farms'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
        return render_template('user_farms.html')
    else:
        pass
    finally:
        pass


    flash('Error in TRY')
    return render_template('user_farms.html')








##################
# USER NEW CROP
##################
@app.route('/user/farm/field/new-crop', methods=['GET', 'POST'])
@app.route('/user/farm/field/new-crop/<farm_id>', methods=['GET'])
@login_required
def user_new_crop(farm_id = None):

    # DYNAMIC FORM
    farm_choices = current_user.farms.all() # FARM CHOICE
    crop_choices = Crop.query.all() # CROP CHOICE


    today = datetime.now()
    in_a_week = today + timedelta(7)
    myDate = PreDateNewCropForm(field_cultivation_start_date = in_a_week)

    form = NewCropForm(obj = myDate)
    if farm_id == None:
        form.farm_choices.choices = [ (farm.id, farm.farm_name) for farm in farm_choices ] # FARM
        form.farm_choices.choices.insert(0, ('0' ,'Choose:'))
    else:
        farm = current_user.farms.filter_by(id = farm_id).first()
        form.farm_choices.choices = [ (farm.id, farm.farm_name) ] # FARM

    form.field_cultivation_crop.choices = [ (crop.id, str.capitalize(crop._name)) for crop in crop_choices ] # CROP
    form.field_cultivation_crop.choices.insert(0, ('0' ,'Choose:'))

    # POST REQUEST
    if form.validate_on_submit():

        # INTERNAL METHODS
        def cm2_to_m2(cm2):
            return cm2 / 10000

        def m2_to_cm2(m2):
            return m2 * 10000

        def num_plants():
            area_in_cm2 = m2_to_cm2(field_cultivation_area) # cm2
            distance_rows_and_columns = sqrt(area_in_cm2) # cm. since we receive an area instead of a shape, we assumed is perfect square
            num_of_rows = (floor(distance_rows_and_columns / crop._space_x))/2 #
            num_of_cols = (floor(distance_rows_and_columns / crop._space_y))/2 # since space of plant and space for walk is the same DIVIDE by 2
            num_of_plants = num_of_rows * num_of_cols
            return num_of_plants

        # USER OBJS
        user_id = current_user.get_id()
        user = User.query.filter_by(id = user_id).first()
        farm = user.farms.filter_by(id = form.farm_choices.data).first()

        # VALIDATE FIELD AREA
        def validate_area():
            farm_area = farm.farm_area # in cm2
            fields_in_farm = farm.fields.all()
            sum_areas = 0

            for each_field in fields_in_farm:
                sum_areas += each_field.field_cultivation_area # in cm2
            new_area = m2_to_cm2(form.field_cultivation_area.data) # in cm2

            result = farm_area - sum_areas - new_area

            if result < 0:
                return False
            return True

        if not validate_area():
            flash('Your new crop area should not exceed the available land on your farm: {}'.format(farm.farm_name))
            return render_template('user_new_crop.html', form=form)

        # Data from Form
        crop = Crop.query.filter_by(id = form.field_cultivation_crop.data).first()
        field_cultivation_area = form.field_cultivation_area.data # in m2
        field_cultivation_start_date = form.field_cultivation_start_date.data
        field_cultivation_state = form.field_cultivation_state.data
        field_cultivation_type = form.field_cultivation_type.data

        # Calculated vars
        field_cultivation_finish_date = field_cultivation_start_date + timedelta(crop._dtg + crop._dtm) # datetime
        field_num_plants = num_plants() # number Integer
        field_projected_yield = crop._yield * field_num_plants # gr
        field_current_yield = 0
        field_water_required_day = field_num_plants * crop._water

        # FIELD OBJS TO DB
        field = Field(  field_name=crop._name,
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
        if user.farms.count() == 1 and user.farms.first().fields.count() == 1 and user.agrimodules.count() > 0: # if first time and first field, set it as the default one
            print('Field default agrimodule system nummer {} was added and type {}'.format(field.id, type(field.id)))
            field.agrimodule = Agrimodule.query.first()
            db.session.commit()

        #SUCESS AND REDIRECT TO DASHBOARD
        flash('You just created a {} in your {}'.format(crop._name, farm.farm_name))
        return redirect(url_for('user_farms'))

    return render_template('user_new_crop.html', form=form)










##################
# USER EDIT CROP
##################
@app.route('/user/farm/field/edit-crop/<field_id>', methods=['GET', 'POST'])
@login_required
def user_edit_crop(field_id):


    # INTERNAL METHODS
    def cm2_to_m2(cm2):
        return cm2 / 10000

    # get farm id from link
    # get field id from link


    field = Field.query.filter_by(id = field_id).first()
    print(field)
    # farm = current_user.farms.filter_by(id = 1).first()
    farm = Farm.query.filter_by(id = field.farm_id).first()
    print(farm)
    crop = field.crops.first()
    print(field.field_cultivation_start_date)

    myField = PreNewCropForm(field_cultivation_area = cm2_to_m2(field.field_cultivation_area),
                            field_cultivation_start_date = field.field_cultivation_start_date,
                            field_cultivation_state = field.field_cultivation_state,
                            field_cultivation_type = field.field_cultivation_type)

    form = NewCropForm(obj=myField)
    form.farm_choices.choices = [ (farm.id, farm.farm_name) ] # FARM
    form.field_cultivation_crop.choices = [ (crop.id, str.capitalize(crop._name)) ] # CROP

    # POST REQUEST
    if form.validate_on_submit():

        def m2_to_cm2(m2):
            return m2 * 10000

        def num_plants(field_cultivation_area, crop):
            area_in_cm2 = m2_to_cm2(field_cultivation_area) # cm2
            distance_rows_and_columns = sqrt(area_in_cm2) # cm. since we receive an area instead of a shape, we assumed is perfect square
            num_of_rows = (floor(distance_rows_and_columns / crop._space_x))/2 #
            num_of_cols = (floor(distance_rows_and_columns / crop._space_y))/2 # since space of plant and space for walk is the same DIVIDE by 2
            num_of_plants = num_of_rows * num_of_cols
            return num_of_plants

        # USER OBJS
        user_id = current_user.get_id()
        user = User.query.filter_by(id = user_id).first()
        farm = user.farms.filter_by(id = form.farm_choices.data).first()

        # VALIDATE FIELD AREA
        def validate_area():
            farm_area = farm.farm_area # in cm2
            fields_in_farm = farm.fields.all()
            sum_areas = 0

            for each_field in fields_in_farm:
                if each_field.id != field.id:
                    sum_areas += each_field.field_cultivation_area # in cm2
            new_area = m2_to_cm2(form.field_cultivation_area.data) # in cm2

            result = farm_area - sum_areas - new_area

            if result < 0:
                return False
            return True

        if not validate_area():
            flash('Your new crop area should not exceed the available land on your farm: {}'.format(farm.farm_name))
            return render_template('user_edit_crop.html', form=form, field_id = field.id)

        # FIELD OBJS TO DB
        field.field_cultivation_area = m2_to_cm2(form.field_cultivation_area.data) # in m2
        field.field_cultivation_start_date = form.field_cultivation_start_date.data
        field.field_cultivation_state = form.field_cultivation_state.data
        field.field_cultivation_type = form.field_cultivation_type.data

        # Calculated vars
        field.field_cultivation_finish_date = field.field_cultivation_start_date + timedelta(crop._dtg + crop._dtm) # datetime
        field.field_num_plants = num_plants(field_cultivation_area = form.field_cultivation_area.data, crop = crop) # number Integer
        field.field_projected_yield = crop._yield * field.field_num_plants # gr
        field.field_water_required_day = field.field_num_plants * crop._water

        # DB COMMANDS
        db.session.commit()

        #SUCESS AND REDIRECT TO DASHBOARD
        flash('You just edited field: {} in your farm: {}'.format(field.field_name, farm.farm_name))
        return redirect(url_for('user_farms'))
    return render_template('user_edit_crop.html', form=form, field_id = field_id)


##################
# USER DELETE CROP
##################
@app.route('/user/farm/field/delete-crop/<field_id>', methods=['GET'])
@login_required
def user_delete_crop(field_id):

    try:
        field_to_del = Field.query.filter_by(id = field_id).first()
        farm = Farm.query.filter_by(id = field_to_del.farm_id).first()
        db.session.delete(field_to_del)
        db.session.commit()
        flash('You just deleted field: {} in your farm: {}'.format(field_to_del.field_name, farm.farm_name))
        return redirect(url_for('user_farms'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
    else:
        pass
    finally:
        pass


    flash('Error in TRY')
    return render_template('user_farms.html')



# AgrimoduleAddSensorForm, PreEditAgrimoduleForm, EditAgrimoduleForm, PreEditAgripumpForm, EditAgripumpForm

###################
# USER NEW AGRIMODULE
###################
@app.route('/user/settings/agrimodule/new', methods=['GET', 'POST'])
@login_required
def user_new_agrimodule():


    def get_farm_name(id):
        return current_user.farms.filter_by(id = id).first().farm_name
    def get_farm_location(id):
        return current_user.farms.filter_by(id = id).first().farm_location
    def cm2_to_m2(cm2):
            return cm2 / 10000

    # Get list of all fields
    farms = current_user.farms.all()
    field_choices = []
    for farm in farms:
        for field in farm.fields.all():
            field_choices.append(field)

    # declare form
    form = NewAgrimoduleForm()
    # add dynamic choices
    form.field_choices.choices = [ (field.id, field.field_name + ' ' + str(cm2_to_m2(field.field_cultivation_area)) + ' m2 ' + get_farm_location(field.farm_id) + ' ' + get_farm_name(field.farm_id)) for field in field_choices ]
    form.field_choices.choices.insert(0, (0 ,'Choose:'))


    if form.validate_on_submit():

        # ADD AGRISYS OBJS
        name = form.name.data
        identifier = form.identifier.data
        lat = form.lat.data
        lon = form.lon.data
        field_choice = form.field_choices.data
        print(name, identifier, lat, lon, field_choice)

        # OBJS TO DB
        agrimodule = Agrimodule(user = current_user,
                                name = name,
                                identifier = identifier,
                                lat = lat,
                                lon = lon,
                                field_id = field_choice)
        print(agrimodule.field_id)

        # DB COMMANDS
        db.session.add(agrimodule)
        db.session.commit()


        # FLASH AND REDIRECT
        flash('You just added a new agrimodule: {}'.format(name))
        return redirect(url_for('user_farms'))
    return render_template('user_new_agrimodule.html', form=form)


##################
# USER EDIT AGRIMODULE
##################
@app.route('/user/settings/agrimodule/edit', methods=['GET', 'POST'])
@app.route('/user/settings/agrimodule/edit/<agrimodule_id>', methods=['GET', 'POST'])
@login_required
def user_edit_agrimodule(agrimodule_id = 0):

    if int(agrimodule_id) <= 0:
        flash('This Agrimodule done not exist.')
        return redirect(url_for('home'))

    agrimodule_to_edit = current_user.agrimodules.filter_by(id = agrimodule_id).first()
    myAgrimodule = PreEditAgrimoduleForm(name = agrimodule_to_edit.name, field_choices = agrimodule_to_edit.field_id)


    form = EditAgrimoduleForm(obj = myAgrimodule)

    farms = current_user.farms.all()
    field_choices = []
    for farm in farms:
        for field in farm.fields.all():
            field_choices.append(field)


    def get_farm_name(id):
        return current_user.farms.filter_by(id = id).first().farm_name
    def get_farm_location(id):
        return current_user.farms.filter_by(id = id).first().farm_location
    def cm2_to_m2(cm2):
            return cm2 / 10000
    form.field_choices.choices = [ (field.id, field.field_name + ' ' + str(cm2_to_m2(field.field_cultivation_area)) + ' m2 ' + get_farm_location(field.farm_id) + ' ' + get_farm_name(field.farm_id)) for field in field_choices ]
    form.field_choices.choices.insert(0, (0 ,'Choose:'))
    form.field_choices.choices.append((1000 ,'Disconnect!'))
    # form.field_choices.choices = [ (field.id, field.field_name + ' ' + str(cm2_to_m2(field.field_cultivation_area)) + ' m2 ' + get_farm_location(field.farm_id) + ' ' + get_farm_name(field.farm_id)) for field in field_choices ]
    if form.validate_on_submit():   # IF request.methiod == 'POST'

        # if agrimodule is already in that field
        def has_agrimodule(field_id):
            if Agrimodule.query.filter_by(field_id = field_id).count() > 0:
                return True
            else:
                return False

        def same_agrimodule(form_field_id, agrimodule_to_edit_pump_id):
            if agrimodule_to_edit_pump_id == form_field_id:
                return True
            else:
                return False


        if same_agrimodule(form.field_choices.data, agrimodule_to_edit.field_id):
            field = Field.query.filter_by(id = form.field_choices.data).first()
            flash('Nothing changed. You are alraedy monitoring the field: {}!'.format(field.field_name))
            return redirect(url_for('user_farms'))

        if has_agrimodule(form.field_choices.data):
            agrimodule = current_user.agrimodules.filter_by(field_id = form.field_choices.data).first()
            flash('That field is being monitored already by agrimodule: {}'.format(agrimodule.name))
            return redirect(url_for('user_edit_agrimodule', form=form, agrimodule_id = agrimodule_id))

        # REST OF FORM HANDLING
        if form.field_choices.data == 0:
            flash('Nothing changed!'.format())
        elif form.field_choices.data == 1000:
            field = Field.query.filter_by(id = agrimodule_to_edit.field_id).first()
            flash('You just disconnected your agrimodule {} from field: {}'.format(agrimodule_to_edit.name, field.field_name))
            agrimodule_to_edit.field_id = None
        else:
            field = Field.query.filter_by(id = form.field_choices.data).first()
            flash('You just change your agrimodule {} to monitor: {}'.format(agrimodule_to_edit.name, field.field_name ))
            agrimodule_to_edit.field_id = form.field_choices.data

        agrimodule_to_edit.name = form.name.data
        db.session.commit()

        return redirect(url_for('user_farms'))
    return render_template('user_edit_agrimodule.html', form=form, agrimodule_to_edit=agrimodule_to_edit)


# '/user/farm/field/agrimodule/add-sensor'
##################
# USER ADD SENSOR
##################
@app.route('/user/farm/field/agrimodule/add-sensor', methods=['GET', 'POST'])
@app.route('/user/farm/field/agrimodule/add-sensor/<agrimodule_id>', methods=['GET', 'POST'])
@login_required
def user_add_sensor(agrimodule_id = 0):

    form = AgrimoduleAddSensorForm()

    if int(agrimodule_id) <= 0:

        agrimodule_choices = current_user.agrimodules.all()
        form.agrimodule_choices.choices = [ (agrimodule.id, agrimodule.name) for agrimodule in agrimodule_choices ] # AGRIMODULE
        form.agrimodule_choices.choices.insert(0, ('0' ,'Choose:'))
    else:
        agrimodule = current_user.agrimodules.filter_by(id = agrimodule_id).first()
        form.agrimodule_choices.choices = [ (agrimodule.id, agrimodule.name) ] # AGRIMODULE





    if form.validate_on_submit():   # IF request.methiod == 'POST'

        agrimodule_id = form.agrimodule_choices.data
        sensor_type = form.sensor_choices.data
        identifier = form.identifier.data

        if sensor_type == 'Agripump':
            agripump = Agripump(agrimodule_id = agrimodule_id, identifier = identifier)
            db.session.add(agripump)

        if sensor_type == 'Agrisensor':
            agrisensor = Agrisensor(agrimodule_id = agrimodule_id, identifier = identifier)
            db.session.add(agrisensor)


        # DB COMMANDS
        db.session.commit()

        flash('You just added an {}: {} in your system: {}'.format(sensor_type, identifier, Agrimodule.query.filter_by(id = agrimodule_id).first().name))
        return redirect(url_for('user_farms'))
    return render_template('user_add_sensor.html', form=form)



# '/user/farm/field/agripump/edit/<agripump_id>'
##################
# USER EDIT AGRIPUMP
##################
@app.route('/user/farm/field/agripump/edit', methods=['GET', 'POST'])
@app.route('/user/farm/field/agripump/edit/<agripump_id>', methods=['GET', 'POST'])
@login_required
def user_edit_agripump(agripump_id = 0):

    # validate thats is an valid id # add later the query if id actually exist
    if int(agripump_id) <= 0:
        flash('This Agripump done not exist.')
        return redirect(url_for('user_farms'))

    # pass to template
    agripump_to_edit = Agripump.query.filter_by(id = agripump_id).first()

    myAgripump = PreEditAgripumpForm(pump_choices = agripump_to_edit.pump_id)
    pump_choices = current_user.pumps.all()

    # Prepopulate form
    form = EditAgripumpForm(obj = myAgripump)
    form.pump_choices.choices = [ (pump.id, pump.pump_name) for pump in pump_choices ] # PUMP
    form.pump_choices.choices.insert(0, (0 ,'Choose:'))
    form.pump_choices.choices.append((1000 ,'Disconnect!'))



    if form.validate_on_submit():   # IF request.methiod == 'POST'
        # FIELD OBJS  TO DB
        try:

            # if agrimodule is already in that field
            def has_agripump(pump_id):
                if Agripump.query.filter_by(pump_id = pump_id).count() > 0:
                    return True
                else:
                    return False
            def same_agripump(form_pump_id, agripump_to_edit_pump_id):
                if agripump_to_edit_pump_id == form_pump_id:
                    return True
                else:
                    return False


            if same_agripump(form.pump_choices.data, agripump_to_edit.pump_id):
                pump = Pump.query.filter_by(id = form.pump_choices.data).first()
                flash('Nothing changed. You are already controlling the pump: {}!'.format(pump.pump_name))
                return redirect(url_for('user_farms'))

            if has_agripump(form.pump_choices.data):
                agripump = Agripump.query.filter_by(pump_id = form.pump_choices.data).first()
                pump = Pump.query.filter_by(id = form.pump_choices.data).first()
                flash('That pump {} is controlled already by agripump: {}'.format(pump.pump_name, agripump.identifier))
                return redirect(url_for('user_edit_agripump', form=form, agripump_id = agripump_id))

            # REST OF FORM HANDLING
            if form.pump_choices.data == 0:
                flash('Nothing changed!'.format())
            elif form.pump_choices.data == 1000:
                pump = current_user.pumps.filter_by(id = agripump_to_edit.pump_id).first()
                flash('You just disconnected your agripump from pump: {}'.format(pump.pump_name))
                agripump_to_edit.pump_id = None
            else:
                pump = current_user.pumps.filter_by(id = form.pump_choices.data).first()
                agripump_to_edit.pump_id = form.pump_choices.data
                flash('You just change your agripumps pump to work on pump: {}'.format(pump.pump_name))

            # DB COMMANDS
            db.session.commit()

            return redirect(url_for('user_farms'))
        except Exception as e:
            flash('Error: ' + str(e))
            print('Error: ' + str(e))
            db.session.rollback()
            return redirect(url_for('user_farms'))
    return render_template('user_edit_agripump.html', form=form, agripump_to_edit = agripump_to_edit)





# '/user/farm/field/agrimodule/delete/<agrimodule_id>'
##################
# USER DELETE AGRIMODULE
##################
@app.route('/user/farm/field/agrimodule/delete', methods=['GET'])
@app.route('/user/farm/field/agrimodule/delete/<agrimodule_id>', methods=['GET'])
@login_required
def user_delete_agrimodule(agrimodule_id = 0):

    if int(agrimodule_id) <= 0:
        flash('This Agrimodule done not exist.')
        return redirect(url_for('user_farms'))

    try:
        agrimodule = current_user.agrimodules.filter_by(id = agrimodule_id).first()

        agripumps = agrimodule.agripumps.all()
        agripumps_qty = agrimodule.agripumps.count()

        agrisensors = agrimodule.agrisensors.all()
        agrisensors_qty = agrimodule.agrisensors.count()

        for agripump in agripumps:
            db.session.delete(agripump)
        for agrisensor in agrisensors:
                db.session.delete(agrisensor)
        db.session.delete(agrimodule)
        db.session.commit()
        flash('You just deleted agrimodule: {}, with {} agripumps and {} agrisensors'.format(agrimodule.name, agripumps_qty, agrisensors_qty))
        return redirect(url_for('user_farms'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
        return render_template('user_farms.html')

    flash('You just deleted agrimodule: {}'.format('agrimodule name'))
    return render_template('user_farms.html')


# '/user/farm/field/agripump/delete/<agripump_id>'
##################
# USER DELETE AGRIPUMP
##################
@app.route('/user/farm/field/agripump/delete', methods=['GET'])
@app.route('/user/farm/field/agripump/delete/<agripump_id>', methods=['GET'])
@login_required
def user_delete_agripump(agripump_id = 0):

    if int(agripump_id) <= 0:
        flash('This Agripump done not exist.')
        return redirect(url_for('user_farms'))

    try:
        agripump_to_del = Agripump.query.filter_by(id = agripump_id).first()
        db.session.delete(agripump_to_del)
        db.session.commit()
        flash('You just deleted agripump: {}'.format(agripump_to_del.identifier))
        return redirect(url_for('user_farms'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
        return render_template('user_farms.html')
    else:
        pass
    finally:
        pass


    flash('Error in user_Delete_Agripump')
    return render_template('user_farms.html')


# '/user/farm/field/agrisensor/delete/<agrisensor_id>'
##################
# USER DELETE AGRISENSOR
##################
@app.route('/user/farm/field/agrisensor/delete', methods=['GET'])
@app.route('/user/farm/field/agrisensor/delete/<agrisensor_id>', methods=['GET'])
@login_required
def user_delete_agrisensor(agrisensor_id = 0):

    try:
        agrisensor_to_del = Agrisensor.query.filter_by(id = agrisensor_id).first()
        db.session.delete(agrisensor_to_del)
        db.session.commit()
        flash('You just deleted agrisensor: {}'.format(agrisensor_to_del.identifier))
        return redirect(url_for('user_farms'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
        return render_template('user_farms.html')
    else:
        pass
    finally:
        pass


    flash('Error in user_Delete_Agripump')
    return render_template('user_farms.html')

###################
# USER ADD PUMP
###################
@app.route('/user/farm/add-pump', methods=['GET', 'POST'])
@login_required
def user_add_pump():

    form = AddPumpForm()
    if form.validate_on_submit():

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
        pump = Pump(user = current_user, pump_name = pump_name, pump_brand = pump_brand, pump_flow_rate = pump_flow_rate, pump_head = pump_head, pump_watts = pump_watts)

        # DB COMMANDS
        db.session.add(pump)
        db.session.commit()

        # FLASH AND REDIRECT
        flash('''Your Pump brand: {}
                Flow rate: {} lps
                Head pressure: {} m
                Wattage: {} kW'''.format(form.pump_brand, form.pump_flow_rate.data, form.pump_head.data, form.pump_watts.data))
        return redirect(url_for('user_farms'))

    return render_template('user_add_pump.html', form=form)


###################
# USER EDIT PUMP
###################
@app.route('/user/farm/edit-pump', methods=['GET', 'POST'])
@app.route('/user/farm/edit-pump/<pump_id>', methods=['GET', 'POST'])
@login_required
def user_edit_pump(pump_id = 0):

    if int(pump_id) <= 0:
        flash('This Pump does not exist.')
        return redirect(url_for('user_farms'))

    def mlpm_to_lps(mlpm):
        return mlpm / (1000 * 60)
    def cm_to_m(cm):
        return cm / 100
    def w_to_kw(w):
        return w / 1000

    pump_to_edit = current_user.pumps.filter_by(id = pump_id).first()


    myPump = PreAddPumpForm(pump_name = pump_to_edit.pump_name, pump_brand = pump_to_edit.pump_brand, pump_flow_rate = mlpm_to_lps(pump_to_edit.pump_flow_rate), pump_head = cm_to_m(pump_to_edit.pump_head), pump_watts = w_to_kw(pump_to_edit.pump_watts))

    form = AddPumpForm(obj = myPump)
    if form.validate_on_submit():

        def lps_to_mlpm(lps):
            return lps * (1000 * 60)
        def m_to_cm(m):
            return m * 100
        def kw_to_w(kw):
            return kw * 1000
        # ADD PUMP OBJS
        pump_to_edit.pump_name = form.pump_name.data
        pump_to_edit.pump_brand = form.pump_brand.data
        pump_to_edit.pump_flow_rate = lps_to_mlpm(form.pump_flow_rate.data)
        pump_to_edit.pump_head = m_to_cm(form.pump_head.data)
        pump_to_edit.pump_watts = kw_to_w(form.pump_watts.data)


        # DB COMMANDS
        db.session.commit()

        # FLASH AND REDIRECT
        flash('''Your Pump brand: {}
                Flow rate: {} lps
                Head pressure: {} m
                Wattage: {} kW'''.format(form.pump_brand, form.pump_flow_rate.data, form.pump_head.data, form.pump_watts.data))
        return redirect(url_for('user_farms'))

    return render_template('user_edit_pump.html', form=form, pump_id = pump_id)


##################
# USER DELETE PUMP
##################
@app.route('/user/farm/delete-pump', methods=['GET'])
@app.route('/user/farm/delete-pump/<pump_id>', methods=['GET'])
@login_required
def user_delete_pump(pump_id = 0):

    if int(pump_id) <= 0:
        flash('Cant delete. This Pump does not exist.')
        return redirect(url_for('user_farms'))

    try:
        pump_to_del = Pump.query.filter_by(id = pump_id).first()
        db.session.delete(pump_to_del)
        db.session.commit()
        flash('You just deleted pump: {}'.format(pump_to_del.pump_name))
        return redirect(url_for('user_farms'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
        return render_template('user_farms.html')
    else:
        pass
    finally:
        pass


    flash('Error in user_delete_pump')
    return render_template('user_farms.html')

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
@app.route('/user/farm/alerts', methods=('GET', 'POST'))
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


##########################################################
##########################################################
# USER SETTINGS VIEWS
##########################################################
##########################################################

##################
# USER PROFILE
##################
@app.route('/user/settings/profile', methods=('GET', 'POST'))
@login_required
def user_profile():
    name = current_user.name
    return render_template('user_profile.html', name=name)

##################
# USER PROFILE EDIT
##################
@app.route('/user/settings/profile/edit', methods=('GET', 'POST'))
@login_required
def user_profile_edit():
    user = User.query.filter_by(email=current_user.email).first()
    # Prepopulate form
    myUser = PreUserProfileForm(username = user.username,
                                name = user.name,
                                last_name = user.last_name,
                                address = user.address,
                                zipcode = user.zipcode,
                                city = user.city,
                                state = user.state,
                                country = user.country,
                                email = user.email,
                                email_rec = user.email_rec,
                                birthday = user.birthday,
                                image = user.image,
                                mobile = user.mobile)
    form = UserProfileForm(obj=myUser)
    # if image is not uploaded it gets a TypeError
    if form.validate_on_submit():   # IF request.methiod == 'POST'
        user = User.query.filter_by(id=current_user.get_id()).first()
        # FIELD OBJS  TO DB
        try:
            # IMAGE HANDLING
            if not form.image.data == user.image:
                image_filename = photos.save(form.image.data)
                image_url = photos.url(image_filename)
                user.image = image_url
            # REST OF FORM HANDLING
            user.username = form.username.data
            user.name = form.name.data
            user.last_name = form.last_name.data
            user.address = form.address.data
            user.zipcode = form.zipcode.data
            user.city = form.city.data
            user.state = form.state.data
            user.country = form.country.data
            user.email = form.email.data
            user.email_rec = form.email_rec.data
            user.birthday = form.birthday.data
            user.mobile = form.mobile.data
            db.session.commit()
        except Exception as e:
            flash(e)
            print(e)
            db.session.rollback()
        flash('You updated sucessfully your profile')
        return redirect(url_for('user_profile'))
    return render_template('user_profile_edit.html', form=form)
