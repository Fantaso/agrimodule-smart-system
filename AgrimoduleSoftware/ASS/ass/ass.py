from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_HASH'] = 'plaintext' # when change later, SALT must be configure too.
app.config['SECURITY_REGISTERABLE'] = True 	# allows register form template from flask-security
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False # to disable sending a confirmation email for registering without configuring the email register yet.
# app.config['SECURITY_LOGIN_URL'] = 'security/login_user.html'
# app.config['SECURITY_REGISTER_URL'] = 'security/register_user.html'
# app.config['SECURITY_RESET_URL'] = 'security/reset_password.html'
# app.config['SECURITY_CHANGE_URL'] = 'security/change_password.html'

# app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
# app.config['SECURITY_PASSWORD_SALT'] = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Volumes/TiroLoco/5.DevEloper/AgrimoduleSmartSystem/AgrimoduleSoftware/ASS/ass/ass.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database connection object
db = SQLAlchemy(app)

# Define models
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
    confirmed_at = db.Column(db.DateTime())
    
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
# @app.before_first_request
# def create_user():
    # db.drop_all()
    # db.create_all()
    # from flask.ext.security.utils import encrypt_password
    # user_datastore.create_user(email='carlos@sv.de', password=encrypt_password('carlos123'))
    # user_datastore.create_user(email='carlos@sv.de', password='carlos123')
    # db.session.commit()
    # return 'USER CREATED'

# Views
@app.route('/')
@login_required
def home():
    return '<h1>hola hola</h1>'
    # return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)