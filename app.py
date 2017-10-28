import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import User, UserAccess, UserList
from resources.report import Report, ReportList
from resources.transport import Transport, TransportList, TransportCreate
from resources.box import Box, BoxList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'EiEiO'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

#Boxes entry points
api.add_resource(Box, '/box/<string:name>')
api.add_resource(BoxList, '/boxes')

#Transports entry points
api.add_resource(Transport, '/transport/<int:transport_id>')
api.add_resource(TransportCreate, '/createtransport')
api.add_resource(TransportList, '/transports')

# Report entry points
api.add_resource(Report, '/report/<int:transport_id>')
api.add_resource(ReportList, '/reports')

# Users entry points
api.add_resource(User, '/user')
api.add_resource(UserList, '/users')
api.add_resource(UserAccess, '/user_access/<string:username>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=8080, debug=True)