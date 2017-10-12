from flask_restful import Resource, reqparse
from models.transport import TransportModel

class Transport(Resource):
    parser = reqparse.RequestParser()
    
    parser.add_argument('organ',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('responsible',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    
    def get(self, transport_id):
        transport = TransportModel.find_by_transport_id(transport_id)
        if transport:
            return transport.json()
        return {'error_message': 'Transport not found'}, 404

    def post(self, transport_id):
        if TransportModel.find_by_transport_id(transport_id):
            return {'error_message': "A transport with transport_id '{}' already exists.".format(transport_id)}, 400

        data = Transport.parser.parse_args()

        transport = TransportModel(data['organ'], data['responsible'])

        try:
            transport.save_to_db()
        except:
            return {"error_message": "An error occurred creating the transport."}, 500

        return transport.json(), 201

    def delete(self, transport_id):
        transport = TransportModel.find_by_transport_id(transport_id)
        if transport:
            transport.delete_from_db()

        return {'success_message': 'Transport deleted'}

class TransportList(Resource):
    def get(self):
        return {'transports': list(map(lambda x: x.json(), TransportModel.query.all()))}