#!/usr/bin/python3

from flask import Flask, request, abort, jsonify
from datetime import datetime, timedelta
import json, os, requests

settingsFile = os.path.join(os.path.dirname(__file__), 'Resources/settings.json')
with open(settingsFile,'r') as sf:
	settings = json.load(sf)
ssl_set = settings["SSL"]
api_set = settings["API"]
ssl_cert_file = ssl_set["cert"]
ssl_key_file = ssl_set["key"]
api_auth = api_set["auth"]
api_check = api_set["auth-secret"]

app = Flask(__name__)

@app.route('/oktalogin', methods=['GET', 'POST'])
def oktalogin():
	if request.method == 'GET':
		auth_key = request.headers['X-Okta-Verification-Challenge']
		return jsonify(
			verification=auth_key
			), 200
	elif request.method == 'POST':
		event_auth = request.headers['Okta-Event-Auth']
		if event_auth == api_check:
			json_data = request.get_json()
			events = json_data["data"]["events"][0]
			user = events["actor"]["alternateId"]
			raw_event_time = json_data["eventTime"]
			event_time = datetime.strptime(raw_event_time, '%Y-%m-%dT%H:%M:%S.%fZ')
			delta = timedelta(hours=5)
			eastern_time = event_time - delta
			formatted_time = f'{eastern_time:%Y-%m-%d %H:%M:%S}'
			print("Secret Auth Successful")
			print('%s logged in on %s' % (user,formatted_time))

			# endpoint = "https://dev-246301.okta.com/api/v1/users/%s" % user
			# headers = {
			# 	"Accept" : "application/json",
			# 	"Content-Type" : "application/json",
			# 	"Authorization" : "%s" % api_auth
			# }
			# data = {"profile" : {"last_login" : formatted_time}}
			# r = requests.post(endpoint, data=json.dumps(data), headers=headers)
			return '', 200
		else:
			return 'Unauthorized', 401
	else:
		abort(400)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', ssl_context=(ssl_cert_file, ssl_key_file))