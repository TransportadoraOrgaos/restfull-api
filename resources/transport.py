from flask_restful import Resource, reqparse
from models.transport import TransportModel

class Transport(Resource):
    def get(self, id):
        transport = TransportModel.find_by_id(id)
        if transport:
            return transport.json()
        return {'error_message': 'Transport not found'}, 404

    def post(self, name):
        if TransportModel.find_by_name(name):
            return {'error_message': "A transport with name '{}' already exists.".format(name)}, 400

        data = Report.parser.parse_args()
        transport = TransportModel(name, data['organ'], data['responsible'])

        try:
            transport.save_to_db()
        except:
            return {"error_message": "An error occurred creating the transport."}, 500

        return transport.json(), 201



        try:
            report.save_to_db()
        except:
            return {"error_message": "An error occurred inserting the report."}, 500

        return report.json(), 201




    def delete(self, name):
        transport = TransportModel.find_by_name(name)
        if transport:
            transport.delete_from_db()

        return {'success_message': 'Transport deleted'}

class TransportList(Resource):
    def get(self):
        return {'transports': list(map(lambda x: x.json(), TransportModel.query.all()))}