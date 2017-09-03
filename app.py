from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

transports = [
	{
		'code' : 'code',
		'updates' : [
			{
				'latitude': -16.013810,
				'longitude': -48.060836,
				'temperature': 2,
				'pressure': 3,
				'is_locked': True,
				'datetime': 'time'
			}
		]
	}

]

@app.route('/') #homepage
def home():
	return render_template('index.html')
	
#post 	/transport data: {code:}
@app.route('/transport', methods=['POST'])
def create_transport():
	request_data = request.get_json()
	new_transport = {
		'code': request_data['code'],
		'updates': []
	}
	transports.append(new_transport)
	return jsonify(new_transport)

#get 	/transport/<string:code>
@app.route('/transport/<string:code>')
def get_transport(code):
	# Iterate over transports
	# If the transport code matches, return it
	# If none match, return an error message
	for transport in transports:
		if transport['code'] == code:
			return jsonify(transport)
	return jsonify({'message': 'Transport not found!'})

#get	/transports
@app.route('/transports')
def get_transports():
	return jsonify({'transports': transports})

#post 	/transport/<string:code>/update  {geopos:, temperature:, pressure:, is_locked:, datetime:}
@app.route('/transport/<string:code>/update', methods=['POST'])
def create_transport_update(code):
	request_data = request.get_json()
	for transport in transports:
		if transport['code'] == code:
			new_update = {
				'latitude': request_data['latitude'],
				'longitude': request_data['longitude'],
				'temperature': request_data['temperature'],
				'pressure': request_data['pressure'],
				'is_locked': request_data['is_locked'],
				'datetime': request_data['datetime']
			}
			transport['updates'].append(new_update)
			return jsonify(new_update)
	return jsonify({'message': 'Transport not found!'})

#get	/transport/<string:code>/updates
@app.route('/transport/<string:code>/updates')
def get_updates_in_transport(code):
	for transport in transports:
		if transport['code'] == code:
			return jsonify({'updates': transport['updates']})
		else:
			return jsonify({'message': 'Transport not found!'})

app.run(port=8080)