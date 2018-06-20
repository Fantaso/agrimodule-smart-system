from flask import Blueprint, render_template, redirect, url_for, flash
from solarvibes.models import User, Agrimodule, Agripump, Measurement, Agrisensor
from flask_login import current_user
from flask_security import login_required
from solarvibes import app, db

agrimodule_api = Blueprint(
    'agrimodule_api',
    __name__,
    template_folder="templates"
)













#### flask-restless basic configuration.
# from flask_restless import APIManager
# manager = APIManager(app, flask_sqlalchemy_db = db)
# manager.create_api(Agrimodule)
# manager.create_api(Agrisensor, methods=['GET'])
# manager.create_api(Agripump, methods=['GET'])
# manager.create_api(Measurement, methods=['GET','POST'])

##################
#
##################
# @agrimodule_api.route('/', methods=['GET'])
# @agrimodule_api.route('/<agrimodule_id>', methods=['GET'])
# @login_required
# def show_agrimodule(agrimodule_id = None):
#
#     if agrimodule_id == None:
#         flash('page not allowed')
#         return redirect(url_for(main.index))
#
#     if Agrimodule.query.filter_by(id=agrimodule_id).first() == None:
#         flash('That agrimodule do NOT exist')
#         return redirect(url_for(main.index))
#
#     user = current_user
#     agrimodule = current_user.agrimodules.filter_by(id = agrimodule_id).first()
#     farm = user.farms.first()
#     # TODO: here is for only 1 crop in the field. but when mix cultivation or multi. need to reflect more than 1 crop
#     field = farm.fields.first()
#     system_name = agrimodule.name
#     crop = field.crops.first()
#     measurement = agrimodule.measurements.order_by(Measurement.timestamp.desc()).first()
#
#     return render_template('agrimodule/show.html', sensor_id = agrimodule_id, sensor = agrimodule, measurement = measurement, crop = crop, farm = farm, field = field, sensortype = 'Agrimodule', system_name = system_name)
#
# ##################
# # USER SHOW AGRISENSOR
# ##################
# @agrimodule_api.route('/<agrimodule_id>/agrisensor', methods=['GET'])
# @agrimodule_api.route('/<agrimodule_id>/agrisensor/<agrisensor_id>', methods=['GET'])
# @login_required
# def show_agrisensor(agrimodule_id = None, agrisensor_id = None):
#
#     if Agrimodule.query.filter_by(id=agrimodule_id).first() == None:
#         flash('That agrimodule do NOT exist')
#         return redirect(url_for(main.index))
#     if Agrisensor.query.filter_by(id=agrisensor_id).first() == None:
#         flash('That agrisensor do NOT exist')
#         return redirect(url_for(main.index))
#
#     if agrimodule_id == None:
#         flash('page not allowed')
#         return redirect(url_for(main.index))
#     if agrisensor_id == None:
#         flash('pag not allowed')
#         return redirect(url_for(main.index))
#
#     user = current_user
#     agrimodule = current_user.agrimodules.filter_by(id = agrimodule_id).first()
#     agrisensor = agrimodule.agrisensors.filter_by(id = agrisensor_id).first()
#     farm = user.farms.first()
#     field = farm.fields.first()
#     system_name = agrimodule.name
#     crop = field.crops.first()
#     measurement = agrimodule.measurements.order_by(Measurement.timestamp.desc()).first()
#
#     return render_template('agrimodule/show.html', sensor_id = agrisensor_id, sensor = agrisensor, measurement = measurement, crop = crop, farm = farm, field = field, sensortype = 'Agrisensor', system_name = system_name)
#
#
# # print (crop._soil_ph_min)
# # print (crop._soil_ph_max)
# # print (crop._soil_temp_min)
# # print (crop._soil_temp_max)
# # print (crop._soil_humi_min)
# # print (crop._soil_humi_max)
# # print (crop._soil_nutrient_min)
# # print (crop._soil_nutrient_max)
# # print (crop._air_temp_min)
# # print (crop._air_temp_max)
# # print (crop._air_humi_min)
# # print (crop._air_humi_max)
#
# # print(ag_measurement.timestamp)
# # print(ag_measurement.soil_ph)
# # print(ag_measurement.soil_nutrient)
# # print(ag_measurement.soil_temp)
# # print(ag_measurement.soil_humi)
# # print(ag_measurement.air_temp)
# # print(ag_measurement.air_humi)
# # print(ag_measurement.air_pres)
# # print(ag_measurement.solar_radiation)
# # print(ag_measurement.batt_status)
# # print(ag_measurement.lat)
# # print(ag_measurement.lon)
