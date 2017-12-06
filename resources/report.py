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
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('longitude',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('temperature',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('is_locked',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('transport_id',
        type=int,
        required=True,
        help="All reports must have a transport_id!"
    )
    parser.add_argument('enable',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, transport_id):
        return {'reports': list(map(lambda x: x.json(), ReportModel.query.filter_by(transport_id=transport_id).all()))}
        #report = ReportModel.find_by_transport_id(transport_id)
        #if report:
        #    return {'reports': [report.json() for report in self.ReportModel.all()]}
        #return {'error_message': 'Report not found'}, 404

    def post(self, transport_id):
        data = Report.parser.parse_args()

        report = ReportModel(
            data['date'], 
            data['latitude'], 
            data['longitude'], 
            data['temperature'], 
            data['is_locked'],
            transport_id,
            data['enable']
        )

        try:
            report.save_to_db()
        except:
            return {"error_message": "An error occurred inserting the report."}, 500

        return report.json(), 201

    @jwt_required()
    def delete(self, transport_id):
        report = ReportModel.find_by_transport_id(transport_id)
        if report:
            for report in report:
                report.delete_from_db()
            return {'success_message': 'Report deleted'}
        return {'error_message': 'Report not encountered'}

class ReportCreate(Resource):
    def post(self):
        data = Report.parser.parse_args()

        report = ReportModel(
            data['date'], 
            data['latitude'], 
            data['longitude'], 
            data['temperature'], 
            data['is_locked'],
            data['transport_id'],
            data['enable']
        )

        try:
            report.save_to_db()
        except:
            return {"error_message": "An error occurred creating the report."}, 500

        return report.json(), 201

class ReportList(Resource):
    def get(self):
        return {'reports': list(map(lambda x: x.json(), ReportModel.query.all()))}