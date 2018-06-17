from flask import Blueprint, render_template, redirect, url_for
from solarvibes.models import User, Agrimodule
from flask_login import current_user
from flask_security import login_required

agrimodule = Blueprint(
    'agrimodule',
    __name__,
    template_folder="templates"
)


##################
# USER AGRIMODULE
##################
@agrimodule.route('/', methods=['GET'])
@login_required
def show():
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

    return render_template('agrimodule/show.html', ag_measure = ag_measure, crop = crop)
