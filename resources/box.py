from flask_restful import Resource, reqparse
from models.box import BoxModel

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
        if box:
            box.delete_from_db()

        return {'success_message': 'Box deleted'}

class BoxList(Resource):
    def get(self,):
        return {'boxes': list(map(lambda x: x.json(), BoxModel.query.all()))}