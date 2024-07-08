from flask import request
from flask_restx import Resource, Namespace, fields
import mysql.connector

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'userName': fields.String(required=True, description='The user name'),
    'userEmail': fields.String(required=True, description='The user email'),
    'userPasswd': fields.String(required=True, description='The user password')
})

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='12345678',
    database='probable'
)

cursor = mydb.cursor(dictionary=True)

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    def get(self):
        """List all users"""
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users, 200

@api.route('/create')  # Define a rota para criar um novo usuário
class CreateUser(Resource):
    @api.doc('create_user')
    @api.expect(user_model)  # Espera um modelo de dados conforme definido em 'user_model'
    def post(self):
        """Create a new user"""
        data = request.get_json()
        try:
            cursor.execute("INSERT INTO users (userName, userEmail, userPasswd) VALUES (%s, %s, %s)", 
                           (data['userName'], data['userEmail'], data['userPasswd']))
            mydb.commit()
            return {'message': 'User created successfully'}, 201
        except Exception as e:
            mydb.rollback()
            return {'message': 'Failed to create user', 'error': str(e)}, 500

@api.route('/<string:userName>')
@api.param('userName', 'The user identifier')
class User(Resource):
    @api.doc('get_user')
    def get(self, userName):
        """Fetch a user given its identifier"""
        cursor.execute(f"SELECT * FROM users WHERE userName = '{userName}'")
        user = cursor.fetchone()
        if user:
            return user, 200
        else:
            return {'message': 'User not found'}, 404

    @api.doc('delete_user')
    def delete(self, userName):
        """Delete a user given its identifier"""
        cursor.execute(f"DELETE FROM users WHERE userName = '{userName}'")
        mydb.commit()
        return {'message': 'User deleted successfully'}, 200

    @api.doc('update_user')
    @api.expect(user_model)
    def put(self, userName):
        """Update a user given its identifier"""
        data = request.json
        update_user = f"UPDATE users SET userName = '{data['userName']}', userEmail = '{data['userEmail']}', userPasswd = '{data['userPasswd']}' WHERE userName = '{userName}'"
        cursor.execute(update_user)
        mydb.commit()
        return {'message': 'User updated successfully'}, 200

@api.route('/<string:userEmail>')
@api.param('userEmail', 'The user email')
class UserByEmail(Resource):
    @api.doc('get_user_by_email')
    def get(self, userEmail):
        """Fetch a user given its email"""
        cursor.execute("SELECT * FROM users WHERE userEmail = %s", (userEmail,))
        user = cursor.fetchone()
        if user:
            return user, 200
        else:
            return {'message': 'User not found'}, 404
