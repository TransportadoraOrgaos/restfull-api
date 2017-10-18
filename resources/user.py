from flask_restful import Resource, reqparse
from models.user import UserModel

class User(Resource):
    #Normal information parser
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('email',
        type=str,
        required=True,
        help="This field cannot be blank."
    )    
    parser.add_argument('access_level',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    #Only username parser
    username_parser = reqparse.RequestParser()
    username_parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    
    def post(self):
        data = User.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"error_message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'], data['email'], data['access_level'])
        user.save_to_db()

        return {"success_message": "User created successfully."}, 201

    def delete(self):
        data = User.username_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            user = UserModel.find_by_username(data['username'])
            if user:
                user.delete_from_db()

            return {'success_message': 'User deleted'}
        else:
            return {'error_message': 'User not found'}

class UserAccess(Resource):
    #Return the acess_level with and username entry
    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return {
                'username': user.username,
                'access_level': user.access_level
            }
        else:
            return {'error_message': 'User not found'}


class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}