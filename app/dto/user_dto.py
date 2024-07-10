from flask_restx import Namespace, fields

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'userName': fields.String(required=True, description='The user name'),
    'userEmail': fields.String(required=True, description='The user email'),
    'userPasswd': fields.String(required=True, description='The user password')
})
