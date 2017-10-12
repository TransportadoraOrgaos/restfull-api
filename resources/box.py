from flask_restful import Resource, reqparse
from models.box import BoxModel
from models.transport import TransportModel
from models.report import ReportModel

class Box(Resource):

    def get(self, name):
        box = BoxModel.find_by_name(name)
        if box:
            return box.json()
        return {'error_message': 'Box not found'}, 404

    def post(self, name):
        if BoxModel.find_by_name(name):
            return {'error_message': "A box with name '{}' already exists.".format(name)}, 400

        box = BoxModel(name)

        try:
            box.save_to_db()
        except:
            return {"error_message": "An error occurred creating the box."}, 500

        return box.json(), 201

    def delete(self, name):
        box = BoxModel.find_by_name(name)
        box_id = box.id
        if box:
            transport = TransportModel.find_by_box_id(box_id)
            if transport:
                for transport in transport:
                    transport_id = transport.id
                    report = ReportModel.find_by_transport_id(transport_id)
                    if report:
                        for report in report:
                            report.delete_from_db()
                    transport.delete_from_db()
            box.delete_from_db()
            return {'success_message': 'Box deleted'}
        else:
            return {'error_message': 'error'}

class BoxList(Resource):
    def get(self,):
        return {'boxes': list(map(lambda x: x.json(), BoxModel.query.all()))}