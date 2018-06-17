from flask import Blueprint, render_template, redirect, url_for
from solarvibes.models import User, Agripump
from flask_login import current_user
from flask_security import login_required

agripump = Blueprint(
    'agripump',
    __name__,
    template_folder="templates"
)


##################
# USER AGRIPUMP
##################
@agripump.route('/', methods=['GET'])
@login_required
def show():

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


    return render_template('agripump/show.html', pump = pump_info, agripump = agripump, field = field, crop = crop, pump_consumption_kwh_per_day=pump_consumption_kwh_per_day)
