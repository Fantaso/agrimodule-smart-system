from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_mail import Mail

from flask_uploads import IMAGES, UploadSet, configure_uploads

from solarvibes.forms import RegisterFormExt



#############################
#############################
# APP
#############################
#############################

app = Flask(__name__)                               # creates the flask app
photos =  UploadSet('photos', IMAGES)               # Flask-Uploads
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'       # Flask-Uploads
app.config.from_pyfile('cfg.cfg')                   # imports app configuration from cfg.cfg
app.config.from_pyfile('cfg2.cfg')                   # imports app configuration from cfg.cfg

configure_uploads(app, photos)

db = SQLAlchemy(app)                                # create database connection object
migrate = Migrate(app, db)                          # creates a migration object for the app db migrations]\
mail = Mail(app)

# TO MANAGE THE MIGRATIONS WITH FLASK-SCRIPT WITH PYTHON EXTERNAL SCRIPTS > goes together to migrations for migraing db
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# HERE STARTS THE MODELS
from solarvibes.models import roles_users, Role, User, Farm, Field, DailyFieldInput, Crop, Pump, Agrimodule, Agrisensor, Measurement, Agripump
# HERE ENDS THE MODELS

#############################
#############################
# Setup Flask-Security
#############################
#############################

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=RegisterFormExt, confirm_register_form=RegisterFormExt)

# HERE STARTS THE ROUTES
from solarvibes import views
from solarvibes.site.views import site
from solarvibes.users.views import users
from solarvibes.welcome.views import welcome
from solarvibes.main.views import main
from solarvibes.settings.views import settings
from solarvibes.farm_settings.views import farm_settings
from solarvibes.agrimodule_settings.views import agrimodule_settings
from solarvibes.pump_settings.views import pump_settings

app.register_blueprint(site, url_prefix='/site')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(welcome, url_prefix='/welcome')
app.register_blueprint(main, url_prefix='/main')
app.register_blueprint(settings, url_prefix='/settings')
app.register_blueprint(farm_settings, url_prefix='/farm_settings')
app.register_blueprint(agrimodule_settings, url_prefix='/agrimodule_settings')
app.register_blueprint(pump_settings, url_prefix='/pump_settings')
# HERE ENDS THE ROUTES
