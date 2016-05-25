import os

from flask import Flask, jsonify, make_response, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from gcm import GCM

app = Flask(__name__)
auth = HTTPBasicAuth()


# [START configs]
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api_prefix = '/notification/api/v1.0'

API_KEY = "AIzaSyDCjtV_krZl39R3pr2PEBurITlR9kGAWTg"
# [END configs]


gcm = GCM(API_KEY)

db = SQLAlchemy(app)

from app import models

auth_test = models.Auth('user', 'pass')


# [START authentication handling]
@auth.get_password
def get_password(username):
    if username == 'koloud':
        return 'MajidSadeghiAlavijeh'
    else:
        return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized Access'}), 403)
# [END authentication handling]


# [START http errors handling]
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
# [END http errors handling]


@app.route('/', methods=['GET'])
def test():
    return "%r" %auth_test


# [START api definitions]
@app.route(api_prefix + '/register_device', methods=['POST'])
def register_device():
    if not request.json or not 'device_token' in request.json or not 'keloud_user' in request.json:
        abort(400)
    token = request.json['device_token']
    user = request.json['keloud_user']
    new_device = models.Device(user, token)

    # Check for device_token, if it exists do nothing
    # if empty
    if not models.Device.query.filter_by(gcm_token=token).all():
        db.session.add(new_device)
        db.session.commit()

    return jsonify({'msg': 'register successful'}), 201


@app.route(api_prefix + '/send_to_devices', methods=['POST'])
@auth.login_required
def send_to_devices():
    if not request.json or not 'keloud_users' in request.json:
        abort(400)

    keloud_users = request.json['keloud_users']
    all_tokens = []
    for user in keloud_users:
        devices = models.Device.query.filter_by(keloud_username=user).all()
        # if tokens was empty, then there isn't any device registered for some user
        # and this should be notified in response
        all_tokens = all_tokens + [device.gcm_token for device in devices]

    data = {'message': request.json.get('msg', "")}
    for d in all_tokens:
        print(type(d))

    # check for all_tokens to not be empty
    gcm_response = gcm.json_request(registration_ids=all_tokens, data=data)

    print(gcm_response)

    return jsonify({'msg': 'send successful'}), 201




# [END api definitions]