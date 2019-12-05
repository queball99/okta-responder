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

app = Flask(__name__)

@app.route('/oktalogin', methods=['GET', 'POST'])
def oktalogin():
	if request.method == 'GET':
		auth_key = request.headers['X-Okta-Verification-Challenge']
		return jsonify(
			verification=auth_key
			), 200
	elif request.method == 'POST':
		json_data = request.get_json()
		events = json_data["data"]["events"][0]
		user = events["actor"]["alternateId"]
		raw_event_time = json_data["eventTime"]
		event_time = datetime.strptime(raw_event_time, '%Y-%m-%dT%H:%M:%S.%fZ')
		delta = timedelta(hours=5)
		eastern_time = event_time - delta
		formatted_time = f'{eastern_time:%Y-%m-%d %H:%M:%S}'
		print('%s logged in on %s' % (user,formatted_time))
		return '', 200
	else:
		abort(400)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', ssl_context=(ssl_cert_file, ssl_key_file))