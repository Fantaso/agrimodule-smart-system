from flask import Blueprint, render_template
from solarvibes.models import Field, Pump
from flask_login import current_user
from flask_security import login_required
from datetime import datetime


main = Blueprint(
    'main',
    __name__,
    template_folder="templates"
)


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():

    # default_farm = Farm.query.filter_by(id = user.default_farm_id).first()
    # //TODO: this should be check somewhere else.its own blueprint
    if current_user.agrimodules.count() == 0:
        flash('welcome for the first time ' + current_user.name + '!')
        print('welcome for the first time, ' + current_user.name + '!')
        set_sys_flag = True
        return 'check //TODO: in main blueprint'
        # return render_template('welcome/welcome.html', current_user=current_user, set_sys_flag=set_sys_flag)
    elif current_user.farms.count() == 0 or current_user.farms.first().fields.count() == 0:
        flash('Now set your farm, ' + current_user.name + '!')
        print('Now set your farm, ' + current_user.name + '!')
        set_sys_flag = False
        return 'check //TODO: in main blueprint'
        # return render_template('welcome/welcome.html', current_user=current_user, set_sys_flag=set_sys_flag)
    else:

        default_farm = current_user.farms.filter_by(_default = 1).one()
        fields = Field.query.filter_by(farm_id = default_farm.id).all()
        pump_db = Pump.query
        return render_template('main/index.html', user=current_user, default_farm = default_farm, fields = fields, pump_db =pump_db, timenow=datetime.now())

    flash('check main blueprint after all conditions!')
    return render_template('main/index.html', user=current_user, default_farm = default_farm, fields = fields, pump_db =pump_db, timenow=datetime.now())
