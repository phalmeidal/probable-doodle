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
    passwd='probable123',
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

    @api.doc('create_user')
    @api.expect(user_model)
    def post(self):
        """Create a new user"""
        data = request.json
        create_user = f"INSERT INTO users (userName, userEmail, userPasswd) VALUES ('{data['userName']}', '{data['userEmail']}', '{data['userPasswd']}')"
        cursor.execute(create_user)
        mydb.commit()
        return {'message': 'User created successfully'}, 201

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
