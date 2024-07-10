from flask import request
from flask_restx import Resource, Namespace, fields
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from models.models import User
from __init__ import db
from datetime import timedelta
from flask_jwt_extended import create_access_token

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'userName': fields.String(required=True, description='The user name'),
    'userEmail': fields.String(required=True, description='The user email'),
    'userPasswd': fields.String(required=True, description='The user password')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    def get(self):
        """List all users"""
        users = User.query.all()
        return [{'userName': user.userName, 'userEmail': user.userEmail, 'userPassword': user.userPasswd} for user in users], 200

@api.route('/create')
class CreateUser(Resource):
    @api.doc('create_user')
    @api.expect(user_model)
    def post(self):
        """Create a new user"""
        data = request.get_json()
        hashed_passwd = bcrypt.hashpw(data['userPasswd'].encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')
        new_user = User(userName=data['userName'], userEmail=data['userEmail'], userPasswd=hashed_passwd)
        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Failed to create user', 'error': str(e)}, 500

@api.route('/<string:userName>')
@api.param('userName', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    def get(self, userName):
        """Fetch a user given its identifier"""
        user = User.query.filter_by(userName=userName).first()
        if user:
            return {'userName': user.userName, 'userEmail': user.userEmail}, 200
        else:
            return {'message': 'User not found'}, 404

    @api.doc('delete_user')
    def delete(self, userName):
        """Delete a user given its identifier"""
        user = User.query.filter_by(userName=userName).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User not found'}, 404

    @api.doc('update_user')
    @api.expect(user_model)
    def put(self, userName):
        """Update a user given its identifier"""
        data = request.get_json()
        user = User.query.filter_by(userName=userName).first()
        if user:
            user.userName = data['userName']
            user.userEmail = data['userEmail']
            user.userPasswd = bcrypt.hashpw(data['userPasswd'], bcrypt.gensalt(10))
            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        else:
            return {'message': 'User not found'}, 404

@api.route('/email/<string:userEmail>')
@api.param('userEmail', 'The user email')
class UserByEmail(Resource):
    @api.doc('get_user_by_email')
    def get(self, userEmail):
        """Fetch a user given its email"""
        user = User.query.filter_by(userEmail=userEmail).first()
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

        user = User.query.filter_by(userEmail=userEmail).first()

        if user and bcrypt.checkpw(userPasswd.encode('utf-8'), user.userPasswd.encode('utf-8')):
            expires = timedelta(hours=1)
            access_token = create_access_token(identity=userEmail, expires_delta=expires)
            
            return {'message': 'Login successful', 'access_token': access_token}, 200
        else:
            return {'message': 'Invalid email or password'}, 401    