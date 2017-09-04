from flask_restful import Resource, reqparse
from models.transport import TransportModel

class Transport(Resource):
    def get(self, name):
        transport = TransportModel.find_by_name(name)
        if transport:
            return transport.json()
        return {'message': 'Transport not found'}, 404

    def post(self, name):
        if TransportModel.find_by_name(name):
            return {'message': "A transport with name '{}' already exists.".format(name)}, 400

        transport = TransportModel(name)
        try:
            transport.save_to_db()
        except:
            return {"message": "An error occurred creating the transport."}, 500

        return transport.json(), 201

    def delete(self, name):
        transport = TransportModel.find_by_name(name)
        if transport:
            transport.delete_from_db()

        return {'message': 'Transport deleted'}

class TransportList(Resource):
    def get(self):
        return {'transports': list(map(lambda x: x.json(), TransportModel.query.all()))}