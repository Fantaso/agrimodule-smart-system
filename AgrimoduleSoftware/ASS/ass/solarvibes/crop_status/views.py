from flask import Blueprint, render_template, redirect, url_for
from solarvibes.models import User
from flask_login import current_user
from flask_security import login_required

crop_status = Blueprint(
    'crop_status',
    __name__,
    template_folder="templates"
)


##################
# USER CROP STATUS
##################
@crop_status.route('/', methods=['GET'])
@login_required
def show():

    user = User.query.filter_by(id = current_user.get_id()).first()
    farm = current_user.farms.first()
    field = farm.fields.first()
    crop = field.crops.first()

    cycle_days_so_far = ( datetime.now() - field.field_cultivation_start_date ).days

    return render_template('crop_status/show.html', crop = crop, field = field, cycle_days_so_far = cycle_days_so_far)
