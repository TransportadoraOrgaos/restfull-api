from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.report import ReportModel

class Report(Resource):
    parser = reqparse.RequestParser()
    
    parser.add_argument('date',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('latitude',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('longitude',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('pressure',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('temperature',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('transport_id',
        type=int,
        required=True,
        help="All reports must have a transport_id!"
    )

    @jwt_required()
    def get(self, transport_id):
        report = ReportModel.find_by_transport_id(transport_id)
        if report:
            return report.json()
        return {'message': 'Report not found'}, 404

    def post(self, transport_id):
        data = Report.parser.parse_args()

        report = ReportModel(data['date'], data['latitude'], data['longitude'], data['pressure'], data['temperature'], data['transport_id'])

        try:
            report.save_to_db()
        except:
            return {"message": "An error occurred inserting the report."}, 500

        return report.json(), 201

    def delete(self, transport_id):
        report = ReportModel.find_by_transport_id(transport_id)
        if report:
            report.delete_from_db()
            return {'message': 'Report deleted'}
        return {'message': 'Report not encountered'}

    def put(self, transport_id):
        data = Report.parser.parse_args()

        report = ReportModel.find_by_transport_id(transport_id)

        if report:
            report.price = data['date']
        else:
            report = ReportModel(transport_id, data['date'])

        report.save_to_db()

        return report.json()

class ReportList(Resource):
    def get(self):
        return {'reports': list(map(lambda x: x.json(), ReportModel.query.all()))}