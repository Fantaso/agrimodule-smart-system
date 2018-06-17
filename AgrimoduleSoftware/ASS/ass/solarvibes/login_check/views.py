from flask import Blueprint, render_template, redirect, url_for, flash, request
from solarvibes import db
from flask_login import current_user
from flask_security import login_required


login_check = Blueprint(
    'login_check',
    __name__,
)


#############################
# INDEX
#############################
@login_check.route('/', methods=['GET'])
@login_required
def index():

    user = current_user
    if  request.method == 'GET':
        # if the user has not yet been authenticated -> goto login
        if user.is_anonymous:
            print('0')
            flash('you must be logged in!')
            return redirect(url_for('login'))

        # if the user is authenticated
        if user.is_authenticated:
            # if is the first time he logs in
            if user.login_count == 1 or user.login_count ==  None:
                print('1')
                user.completed_welcome = False
                db.session.commit()
                return redirect(url_for('welcome.index'))
            # if the user already complete the welcome setup
            if user.completed_welcome:
                print('2')
                return redirect(url_for('main.index'))
            else:
                print('3')
                return redirect(url_for('welcome.index'))
