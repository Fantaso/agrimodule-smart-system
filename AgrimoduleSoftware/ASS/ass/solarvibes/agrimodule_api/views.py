from flask import Blueprint, jsonify, request, make_response
from solarvibes.models import User, Agrimodule, Agripump, Measurement, Agrisensor
from flask_login import current_user
from flask_security import login_required
from solarvibes import app, db
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

agrimodule_api = Blueprint(
    'agrimodule_api',
    __name__,
    template_folder="templates"
)



@agrimodule_api.route('/', methods = ['GET'])
# @login_required
def index():
    return jsonify({'welcome':'check the API to play with Solarvibes!'})


# TODO: roles and authentication for current user must be done in order to retreive users agrimodules
@agrimodule_api.route('/agrimodules', methods = ['GET'])
# @login_required
def get_agrimodules():

    agrimodules = User.query.filter_by(id = 1).first().agrimodules.all()

    # create an empty list
    payload = list()
    for agrimodule in agrimodules:
        # add a dictionary per agrimodule into the list
        payload.append(dict( id = agrimodule.id,
                        system_name = agrimodule.name,
                        user_id = agrimodule.user_id,
                        field_id = agrimodule.field_id,
                        ))

    # make a dictionary as main key 'agrimodules' with a the list of dictionaries to be jsonify
    payload = dict(agrimodules = payload)
    return jsonify(payload)


@agrimodule_api.route('/agrimodule', methods = ['GET'])
@agrimodule_api.route('/agrimodule/<agrimodule_id>', methods = ['GET'])
@login_required
def get_agrimodule(agrimodule_id = None):

    if not agrimodule_id:
        print(agrimodule_id)
        return jsonify({'message':'agrimodule do not exist!'})

    agrimodule = current_user.agrimodules.filter_by(id = agrimodule_id).one()
    return jsonify(agrimodule)



#############################################################################################################################
#############################################################################################################################
########################                      SET MEASUREMENT
#############################################################################################################################
#############################################################################################################################
@agrimodule_api.route('/register/<identifier>', methods = ['POST'])
# @login_required
def register(identifier = None):

    if not identifier:
        print(identifier)
        return jsonify(dict(message = 'registration not allowed!'))

    agrimodule = AgrimoduleList.query.filter_by(identifier = identifier).first()
    if not agrimodule:
        return jsonify(dict(message = 'agrimodule not registered in Solarvibes!'))
    if not agrimodule.has_user_registered:
        return jsonify(dict(message = 'agrimodule has not been registered by farmer!'))

    

# identifier
# type
# has_user_registered
# user_id
# has_agrimodule_registered

    if request.method == 'POST':
        try:
            payload = request.get_json()
            measurement = Measurement(  agrimodule_id = int(payload['agrimodule_id']),
                                        timestamp = datetime(payload['timestamp']),
                                        soil_ph = float(payload['soil_ph']),
                                        soil_nutrient = float(payload['soil_nutrient']),
                                        soil_temp = float(payload['soil_temp']),
                                        soil_humi = float(payload['soil_humi']),
                                        air_temp = float(payload['air_temp']),
                                        air_humi = float(payload['air_humi']),
                                        air_pres = float(payload['air_pres']),
                                        solar_radiation = float(payload['solar_radiation']),
                                        batt_status = int(payload['batt_status']),
                                        lat = float(payload['lat']),
                                        lon = float(payload['lon']),
                                        )
            # set agrimodule with lates batt_status, lat and lon
            agrimodule.batt_status = int(payload['batt_status'])
            agrimodule.lat = float(payload['lat'])
            agrimodule.lon = float(payload['lon'])
            # add object to db and save
            db.session.add(measurement)
            db.session.commit()
            return jsonify({'message':'measurement created!'})
        except:
            db.session.rollback()
            return jsonify({'error':'measurement not created!'})



#############################################################################################################################
#############################################################################################################################
########################                      SET MEASUREMENT
#############################################################################################################################
#############################################################################################################################
@agrimodule_api.route('/agrimodule/<agrimodule_id>/set-measurement', methods = ['POST'])
# @login_required
def set_measurement(agrimodule_id = None):

    if not agrimodule_id:
        print(agrimodule_id)
        return jsonify(dict(message = 'not allowed!'))

    agrimodule = Agrimodule.query.filter_by(id = agrimodule_id).first()
    if not agrimodule:
        return jsonify(dict(message = 'agrimodule do not exist!'))


    data = request.get_json()
    print(data)
    print(request.data)
    print(type(data['agrimodule_id']))
    print(data['timestamp'])
    print(type(data['timestamp']))
    print(type(data['soil_ph']))
    print(type(data['soil_nutrient']))
    print(type(data['soil_temp']))
    print(type(data['soil_humi']))
    print(type(data['air_temp']))
    print(type(data['air_humi']))
    print(type(data['air_pres']))
    print(type(data['solar_radiation']))
    print(type(data['batt_status']))
    print(type(data['lat']))
    print(type(data['lon']))
    if request.method == 'POST':
        try:
            payload = request.get_json()
            measurement = Measurement(  agrimodule_id = int(payload['agrimodule_id']),
                                        timestamp = datetime(payload['timestamp']),
                                        soil_ph = float(payload['soil_ph']),
                                        soil_nutrient = float(payload['soil_nutrient']),
                                        soil_temp = float(payload['soil_temp']),
                                        soil_humi = float(payload['soil_humi']),
                                        air_temp = float(payload['air_temp']),
                                        air_humi = float(payload['air_humi']),
                                        air_pres = float(payload['air_pres']),
                                        solar_radiation = float(payload['solar_radiation']),
                                        batt_status = int(payload['batt_status']),
                                        lat = float(payload['lat']),
                                        lon = float(payload['lon']),
                                        )
            # set agrimodule with lates batt_status, lat and lon
            agrimodule.batt_status = int(payload['batt_status'])
            agrimodule.lat = float(payload['lat'])
            agrimodule.lon = float(payload['lon'])
            # add object to db and save
            db.session.add(measurement)
            db.session.commit()
            return jsonify({'message':'measurement created!'})
        except:
            db.session.rollback()
            return jsonify({'error':'measurement not created!'})

    return jsonify(dict(message = 'FANTASO ERROR'))

#############################################################################################################################
#############################################################################################################################
########################                      GET MEASUREMENT
#############################################################################################################################
#############################################################################################################################
@agrimodule_api.route('/agrimodule/<agrimodule_id>/get-measurement', methods = ['GET'])
@agrimodule_api.route('/agrimodule/<agrimodule_id>/get-measurement/<measurement_id>', methods = ['GET'])
# @login_required
def get_measurement(agrimodule_id = None, measurement_id = None):



    if not agrimodule_id or not measurement_id:
        print(agrimodule_id, measurement_id)
        return jsonify(dict(message = 'not allowed!'))

    agrimodule = Agrimodule.query.filter_by(id = agrimodule_id).first()
    if not agrimodule:
        return jsonify(dict(message = 'agrimodule do not exist!'))

    measurement = agrimodule.measurements.filter_by(id = measurement_id).first()
    if not measurement:
        return jsonify(dict(message = 'measurement do not belong to agrimodule!'))

    if request.method == 'GET':
        try:
            # create a dict with data from db
            payload = dict( measurement_id = measurement.id,
                            agrimodule_id = measurement.agrimodule_id,
                            timestamp = measurement.timestamp,
                            soil_ph = measurement.soil_ph,
                            soil_nutrient = measurement.soil_nutrient,
                            soil_temp = measurement.soil_temp,
                            soil_humi = measurement.soil_humi,
                            air_temp = measurement.air_temp,
                            air_humi = measurement.air_humi,
                            air_pres = measurement.air_pres,
                            solar_radiation = measurement.solar_radiation,
                            batt_status = measurement.batt_status,
                            lat = measurement.lat,
                            lon = measurement.lon,
                            )

            # make a dictionary as main key 'measurement' with a the list of dictionaries to be jsonify
            payload = dict(measurement = payload)
            return jsonify(payload)
        except:
            return jsonify({'error':'measurement corrupted!'})



#############################################################################################################################
#############################################################################################################################
########################                      GET MEASUREMENTS
#############################################################################################################################
#############################################################################################################################
@agrimodule_api.route('/agrimodule/<agrimodule_id>/get-measurements', methods = ['GET'])
@login_required
def get_measurements(agrimodule_id = None):

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if not agrimodule_id:
        print(agrimodule_id)
        return jsonify(dict(message = 'not allowed!'))

    agrimodule = Agrimodule.query.filter_by(id = agrimodule_id).first()
    if not agrimodule:
        return jsonify(dict(message = 'agrimodule do not exist!'))

    measurement = agrimodule.measurements.first()
    if not measurement:
        return jsonify(dict(message = 'agrimodule have not recoreded a measurement!'))

    measurements = agrimodule.measurements.all()

    if request.method == 'GET':
        try:
            # create an empty list
            payload = list()
            for measurement in measurements:
                # add a dictionary per agrimodule into the list
                payload.append(dict(    measurement_id = measurement.id,
                                        agrimodule_id = measurement.agrimodule_id,
                                        timestamp = measurement.timestamp,
                                        soil_ph = measurement.soil_ph,
                                        soil_nutrient = measurement.soil_nutrient,
                                        soil_temp = measurement.soil_temp,
                                        soil_humi = measurement.soil_humi,
                                        air_temp = measurement.air_temp,
                                        air_humi = measurement.air_humi,
                                        air_pres = measurement.air_pres,
                                        solar_radiation = measurement.solar_radiation,
                                        batt_status = measurement.batt_status,
                                        lat = measurement.lat,
                                        lon = measurement.lon,
                                        ))

            # make a dictionary as main key 'measurements' with a the list of dictionaries to be jsonify
            payload = dict(measurements = payload)
            return jsonify(payload)
        except:
            return jsonify({'error':'all measurements corrupted!'})





#### flask-restless basic configuration.
# from flask_restless import APIManager
# manager = APIManager(app, flask_sqlalchemy_db = db)
# manager.create_api(Agrimodule)
# manager.create_api(Agrisensor, methods=['GET'])
# manager.create_api(Agripump, methods=['GET'])
# manager.create_api(Measurement, methods=['GET','POST'])

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
