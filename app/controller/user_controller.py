from flask import request
from flask_restx import Resource
from dto.user_dto import api, user_model
from service.user_service import UserService
from datetime import timedelta
from flask_jwt_extended import create_access_token

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    def get(self):
        users = UserService.get_all_users()
        return [{'user_name': user.user_name, 'user_email': user.user_email, 'user_password': user.user_passwd} for user in users], 200

@api.route('/create')
class CreateUser(Resource):
    @api.doc('create_user')
    @api.expect(user_model)
    def post(self):
        data = request.get_json()
        return UserService.create_user(data)

@api.route('/<string:user_name>')
@api.param('user_name', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    def get(self, user_name):
        user = UserService.get_user_by_name(user_name)
        if user:
            return {'user_name': user.user_name, 'user_email': user.user_email}, 200
        else:
            return {'message': 'User not found'}, 404

    @api.doc('delete_user')
    def delete(self, user_name):
        user = UserService.get_user_by_name(user_name)
        if user:
            return UserService.delete_user(user)
        else:
            return {'message': 'User not found'}, 404

    @api.doc('update_user')
    @api.expect(user_model)
    def put(self, user_name):
        data = request.get_json()
        user = UserService.get_user_by_name(user_name)
        if user:
            return UserService.update_user(user, data)
        else:
            return {'message': 'User not found'}, 404

@api.route('/email/<string:user_email>')
@api.param('user_email', 'The user email')
class UserByEmail(Resource):
    @api.doc('get_user_by_email')
    def get(self, user_email):
        user = UserService.get_user_by_email(user_email)
        if user:
            return {'userName': user.user_name, 'userEmail': user.user_email}, 200
        else:
            return {'message': 'User not found'}, 404

@api.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        user_email = data.get('user_email')
        user_passwd = data.get('user_passwd')

        user = UserService.check_login(user_email, user_passwd)

        if user:
            expires = timedelta(hours=1)
            access_token = create_access_token(identity=user_email, expires_delta=expires)
            return {'message': 'Login successful', 'access_token': access_token}, 200
        else:
            return {'message': 'Invalid email or password'}, 401
