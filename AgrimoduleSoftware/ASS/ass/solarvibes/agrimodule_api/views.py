from flask import Blueprint, jsonify, request, make_response
from solarvibes.models import User, Agrimodule, Agripump, Measurement, Agrisensor
from solarvibes.models import AgrimoduleList
from flask_login import current_user
from flask_security import login_required
from solarvibes import app, db
from flask_restful import Api, Resource
#register the endpoint

import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#############################################################################################################################
########################                      Blueprint
#############################################################################################################################
agrimodule_api = Blueprint('api', __name__)


#############################################################################################################################
########################                      Api OBJ
#############################################################################################################################
api = Api(agrimodule_api)


#############################################################################################################################
########################                      INDEX
#############################################################################################################################
class Index(Resource):
    def get(self):
        return {'Welcome':'This is the Solarvibes API design for the agrimodules to interact with Solarvibes servers!'}


#############################################################################################################################
########################                      0 - HELLO
#############################################################################################################################
class Check(Resource):
    def get(self, identifier):
        # initial validation for whene a request contains no identifier
        if not identifier:
            print(identifier)
            return {'message' : 'Bad request!'}, 400

        try:
            # initialization of variables to be returned
            http_status = 202
            payload = dict(belong_to_user = False,
                            being_used = False,
                            message = 'You have not been bought or registered in a farmer account yet!',
                            )

            # query to retrieve the agrimodule registry - where the flags and to which user in the account the agrimodule belongs to.
            # db exclusive for license and tranfer of ownership of agrimodule
            agrimodule_reg = AgrimoduleList.query.filter_by(identifier = identifier).first()

            # check if identifier even exist // if this agrmiodule has a license mto access the app
            # if not  the answer is return directly here, because the other validation would give an error since agrimodule_reg would a Nonetype obj and it would not ahve atrributes
            if not agrimodule_reg:
                http_status = 403
                payload.update(message = 'Contact Solarvibes: Agrimodule Support!')
                return payload, http_status

            # if a user has registered the agrimodule to his account
            if agrimodule_reg.has_user_registered:
                http_status = 206
                payload.update(message = 'Yes, you have an owner', belong_to_user = True)

            # if a user has registered, may have deleted from its configuration, and there is not point of sending data nowhere
            agrimodule = Agrimodule.query.filter_by(identifier = identifier).first()
            if agrimodule:
                http_status = 200
                payload.update(message = 'Yes, you have an owner and your are being used', being_used = True)

            # validation to sen
            return payload, http_status
        except:
            # in case of exceptions, return a internal server error 500
            return {'error':'Internal server error agrimodule API - FIRST CONTACT!'}, 500


#############################################################################################################################
########################                      Resource resgistration and blueprint
#############################################################################################################################
api.add_resource(Index, '/')
api.add_resource(Check, '/check/<identifier>')

####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################

# ERRORS
# 200, OK
# 201, Created
# 202, Accepted
# 403, Forbidden
# 206, Partial Content
