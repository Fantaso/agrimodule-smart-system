from flask import Flask, render_template, session, request, redirect, url_for, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_migrate import Migrate

from flask_login import current_user

from flask_mail import Mail, Message

from sqlalchemy.sql import func

from forms import EmailForm, EmailAndTextForm, ContactUsForm, RegisterFormExt, FarmForm, FieldForm

#############################
#############################
# APP
#############################
#############################

app = Flask(__name__)               # creates the flask app
app.config.from_pyfile('cfg.cfg')   # imports app configuration from cfg.cfg
db = SQLAlchemy(app)                # create database connection object
Migrate(app, db)                    # creates a migration object for the app db migrations]\
mail = Mail(app)


#############################
#############################
# WEBSITE MODELS
#############################
#############################

class NewsletterTable(db.Model):
    __tablename__ = 'newslettertable'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))

class AgrimoduleFBTable(db.Model):
    __tablename__ = 'agrimodulefbtable'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    msg = db.Column(db.Text(length=1000))

class PlatformFBTable(db.Model):
    __tablename__ = 'platformfbtable'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    msg = db.Column(db.Text(length=1000))

class WorkWithUsTable(db.Model):
    __tablename__ = 'workwithustable'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    msg = db.Column(db.Text(length=1000))

class ContactUsTable(db.Model):
    __tablename__ = 'contactustable'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    msg = db.Column(db.Text(length=1000))


#############################
#############################
# USER MODELS FLASK-SECURITY
#############################
#############################

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    last_name = db.Column(db.String(15))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    birthday = db.Column(db.DateTime(timezone=True), nullable=True)
    mobile = db.Column(db.String(12), unique=True)

    last_login_at = db.Column(db.DateTime(timezone=True))
    current_login_at = db.Column(db.DateTime(timezone=True))
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)

    active = db.Column(db.Boolean(), nullable=True)
    confirmed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    # RELATIONSHIP
    # USER[1]-FARM[M]
    farms = db.relationship('Farm', backref='user', lazy='dynamic')
    # USER[1]-AGRIMODULESYSTEM[M]
    agrimodule_systems = db.relationship('AgrimoduleSystem', backref='user', lazy='dynamic')
    # USER[1]-PUMP[M]
    pumps = db.relationship('Pump', backref='user', lazy='dynamic')

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<user {}>'.format(self.email)


#############################
#############################
# FARMS AND AGRIMODULE MODELS
#############################
#############################

class Farm(db.Model):
    """Farms Models for Users to create. One User can created as many farms as he wants"""
    __tablename__ = 'farm'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    location = db.Column(db.String(20))
    cultivation_area = db.Column(db.Float(precision=2))
    cultivation_process = db.Column(db.String(20))

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
    __tablename__ = 'field'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    cultivation_area = db.Column(db.Float(precision=2))
    cultivation_start_date = db.Column(db.DateTime(timezone=True))
    cultivation_finish_date = db.Column(db.DateTime(timezone=True))
    _current_yield = db.Column(db.Float(precision=2))
    cultivation_state = db.Column(db.String(20))
    cultivation_type = db.Column(db.String(5))

    # RELATIONSHIP
    # FIELD[M]-CROP[M]
    crops = db.relationship('Crop', secondary='crops_field', backref='field', lazy='dynamic')
    # FARM[1]-FIELD[M]
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))
    
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<field {}>'.format(self.name)

class Crop(db.Model):
    '''The crop database reference from farmers or Users.model that can be be cultivated in the Field.Model'''
    __tablename__ = 'crop'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(25), unique=True, nullable=False)
    _variety = db.Column(db.String(25))
    _family = db.Column(db.String(25))
    _yield = db.Column(db.Float(precision=3))
    _space_x = db.Column(db.Float(precision=2))
    _space_y = db.Column(db.Float(precision=2))
    _space_z = db.Column(db.Float(precision=2))
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
    _dtg = db.Column(db.Integer)
    _dtm = db.Column(db.Integer)
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

class Pump(db.Model):
    """pump database used for each field or each agripump whichi is installed in the farm. one farm can ahve as many pump the want as long as the have an agripump for it"""
    __tablename__ = 'pump'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(25))
    flow_rate = db.Column(db.Float(precision=2), nullable=False)
    height_max = db.Column(db.Float(presicion=2), nullable=False)
    kwh = db.Column(db.Float(precision=2), nullable=False)

    # RELATIONSHIP
    # USER[1]-PUMP[M]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # PUMP[1]-AGRIPUMP
    agripumps = db.relationship('Agripump', backref='pump', lazy='dynamic')
    
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<pump {}>'.format(self.brand)   

class AgrimoduleSystem(db.Model):
    """Each agrimodule smart system is unique and has am agrimodule an agripump and maybe agresiensor and other agripumps depending on the complaexity of the farm
    and can be added to any user any farm with a unique identuifier which can connect the data being sent to server to an specific User.Model/Field.Model
    Each agrimodule"""
    __tablename__ = 'agrimodulesystem'
    id = db.Column(db.Integer, primary_key=True)
    _identifier_agrimodulesystem = db.Column(db.String(50), unique=True, nullable=False)
    _identifier_agrimodule = db.Column(db.String(50), unique=True, nullable=False)
    _identifier_agripump = db.Column(db.String(50), unique=True, nullable=False)
    # LOCATION
    _lat_agrimodule = db.Column(db.Float(precision=8))
    _lon_agrimodule = db.Column(db.Float(precision=8))
    _lat_agrisensor = db.Column(db.Float(precision=8))
    _lon_agrisensor = db.Column(db.Float(precision=8))
    _lat_agripump = db.Column(db.Float(precision=8))
    _lon_agripump = db.Column(db.Float(precision=8))

    # RELATIONSHIP
    # AGRIMODULESYSTEM[1]-AGRIMODULE[M]
    agrimodules = db.relationship('Agrimodule', backref='agrimodulesystem', lazy='dynamic')
    # AGRIMODULESYSTEM[1]-AGRIPUMP[M]
    agripumps = db.relationship('Agripump', backref='agrimodulesystem', lazy='dynamic')
    # USER[1]-AGRIMODULESYSTEM[M]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<agrimodulesystem {}>'.format(self.identifier)

class Agrimodule(db.Model):
    """each agrimodule has a different table where all data that is measured by agrimodule is saved in this model"""
    __tablename__ = 'agrimodule'
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
    # AGRIMODULESYSTEM[1]-AGRIMODULE[M]
    agrimodulesystem_id = db.Column(db.Integer, db.ForeignKey('agrimodulesystem.id'))

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<agrimodule {}>'.format(self.date)

class Agripump(db.Model):
    """pump schedule for each farm and agripump, it requires to know which Pump.Model is used in order to make the calculations"""
    __tablename__ = 'agripump'
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
    # AGRIMODULESYSTEM[1]-AGRIPUMP[M]
    agrimodulesystem_id = db.Column(db.Integer, db.ForeignKey('agrimodulesystem.id'))
    # PUMP[1]-AGRIPUMP[M]
    pump_id = db.Column(db.Integer, db.ForeignKey('pump.id'))
    
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<agripump {}>'.format(self.brand)   


#############################
#############################
# Setup Flask-Security
#############################
#############################

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=RegisterFormExt, confirm_register_form=RegisterFormExt)

# Views
# @app.before_request
# def before_request():
#     if session is not None:
#         session = None

#############################
#############################
# WEBSITE VIEWS
#############################
#############################

@app.route('/', methods=('GET', 'POST'))
def index():
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

@app.route('/dashboard', methods=['GET'])
# @login_required
def dashboard():
    if request.method == 'GET':
        if current_user.is_authenticated:
            uid = current_user.get_id()
            username
            return redirect(url_for('dashboard_id', id=uid))
        if current_user.is_anonymous:
            return 'User has not logged in'
        else:
            return 'fuck off'


@app.route('/dashboard/<int:id>', methods=['GET', 'POST'])
@login_required
def dashboard_id(id):
    uid = User.query.filter_by(id=id).first()
    if request.method == 'GET':
        farm_already = Farm.query.all()
        if farm_already == None:
            # this is the first time you join solarvibes, please SETUP your first farm to start
            return render_template('dashboard_init.html', name=uid.name, last_name=uid.last_name, email=uid.email)
        else:
            # if farm exist, deliver the first farm or default one. sending the context of Farm.Model
            return render_template('dashboard.html', name=uid.name, last_name=uid.last_name, email=uid.email)
    if request.method == 'POST':
        return 'POST in dashboard_id'
    else:
        return 'ELSE: in dashboard_id'

#############################
#############################
# APP FARM SETUP VIEWS
#############################
#############################

@app.route('/farm', methods=('GET', 'POST'))
@login_required
def farm():
    if 'farm' not in session:
        session['farm'] = dict()
        session.modified = True
    
    form = FarmForm()               # CREATE WTForm FORM
    if form.validate_on_submit():   # IF request.methiod == 'POST'
        # USER OBJS
        user = current_user
        user_id = user.get_id()
        user_name = User.query.filter_by(id=user_id).first().name
        # FARM OBJS
        name = form.name.data
        location = form.location.data
        cultivation_area = form.cultivation_area.data
        cultivation_process = form.cultivation_process.data
        # FARM OBJS  TO DB
        farm = Farm(    user=user,
                        name=name,
                        location=location,
                        cultivation_area=cultivation_area,
                        cultivation_process=cultivation_process)
        # DB COMMANDS
        db.session.add(farm)
        db.session.commit()
        # OBJS SAVE ON SESSION
        session['farm'] = {'user_id':user_id,
                            'user_name':user_name,
                            'farm_name':name,
                            'farm_location':location,
                            'farm_cultivation_area':cultivation_area,
                            'farm_cultivation_process':cultivation_process}
        session.modified = True
        #SUCESS AND REDIRECT TO NEXT STEP
        flash('You just created farm named: {}'.format(name))
        return redirect(url_for('field'))

    return render_template('farm.html', form=form)

@app.route('/field', methods=('GET', 'POST'))
@login_required
def field():
    print('session "farm" in Field: {}'.format(session['farm']))
    for farm in session['farm']:
        for key, val in farm.items():
            print (val)
    # pre_contact = PreContactUsForm('Carlos','carlos@sv.de','+176-55858585','I would like to get a quotation for my farm 1 hectare located in Berlin')
    form = FieldForm()              # CREATE WTForm FORM
    if form.validate_on_submit():   # IF request.methiod == 'POST'
        # USER OBJS
        user = User.query.filter_by(id = current_user.get_id()).first()
        farm = user.farms.filter_by(name = session['farm']['farm_name']).first()
        crop = Crop.query.filter_by(_name = form.cultivation_crop.data).first()
        # FIELD OBJS
        name = form.name.data
        cultivation_area = form.cultivation_area.data
        cultivation_crop = form.cultivation_crop.data
        cultivation_start_date = form.cultivation_start_date.data
        cultivation_state = form.cultivation_state.data
        cultivation_type = form.cultivation_type.data
        # FIELD OBJS  TO DB
        field = Field(  name=name,
                        farm=farm,
                        cultivation_area=cultivation_area,
                        cultivation_start_date=cultivation_start_date,
                        cultivation_state=cultivation_state,
                        cultivation_type=cultivation_type)
        field.crops.append(crop)
        # DB COMMANDS
        db.session.add(field)
        db.session.commit()
        #SUCESS AND REDIRECT TO DASHBOARD
        flash('You just created a {} in your {}'.format(name, farm.name))
        del session['farm']     # ERASE SESSION OBJS
        return redirect(url_for('main'))

    return render_template('field.html', form=form)


@app.route('/main', methods=('GET', 'POST'))
@login_required
def main():
    return 'congrats'


if __name__ == '__main__':
    app.run()
    # app.run(
    #     host = '192.168.1.4',
    #     port = 8080
    #     )