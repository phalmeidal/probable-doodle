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
        return [{'userName': user.userName, 'userEmail': user.userEmail, 'userPassword': user.userPasswd} for user in users], 200

@api.route('/create')
class CreateUser(Resource):
    @api.doc('create_user')
    @api.expect(user_model)
    def post(self):
        data = request.get_json()
        return UserService.create_user(data)

@api.route('/<string:userName>')
@api.param('userName', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    def get(self, userName):
        user = UserService.get_user_by_name(userName)
        if user:
            return {'userName': user.userName, 'userEmail': user.userEmail}, 200
        else:
            return {'message': 'User not found'}, 404

    @api.doc('delete_user')
    def delete(self, userName):
        user = UserService.get_user_by_name(userName)
        if user:
            return UserService.delete_user(user)
        else:
            return {'message': 'User not found'}, 404

    @api.doc('update_user')
    @api.expect(user_model)
    def put(self, userName):
        data = request.get_json()
        user = UserService.get_user_by_name(userName)
        if user:
            return UserService.update_user(user, data)
        else:
            return {'message': 'User not found'}, 404

@api.route('/email/<string:userEmail>')
@api.param('userEmail', 'The user email')
class UserByEmail(Resource):
    @api.doc('get_user_by_email')
    def get(self, userEmail):
        user = UserService.get_user_by_email(userEmail)
        if user:
            return {'userName': user.userName, 'userEmail': user.userEmail}, 200
        else:
            return {'message': 'User not found'}, 404

@api.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        userEmail = data.get('userEmail')
        userPasswd = data.get('userPasswd')

        user = UserService.check_login(userEmail, userPasswd)

        if user:
            expires = timedelta(hours=1)
            access_token = create_access_token(identity=userEmail, expires_delta=expires)
            return {'message': 'Login successful', 'access_token': access_token}, 200
        else:
            return {'message': 'Invalid email or password'}, 401
