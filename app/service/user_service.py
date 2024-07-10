import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from model.user_model import User
from __init__ import db

class UserService:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_name(userName):
        return User.query.filter_by(userName=userName).first()

    @staticmethod
    def get_user_by_email(userEmail):
        return User.query.filter_by(userEmail=userEmail).first()

    @staticmethod
    def create_user(data):
        hashed_passwd = bcrypt.hashpw(data['userPasswd'].encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')
        new_user = User(userName=data['userName'], userEmail=data['userEmail'], userPasswd=hashed_passwd)
        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Failed to create user', 'error': str(e)}, 500

    @staticmethod
    def update_user(user, data):
        user.userName = data['userName']
        user.userEmail = data['userEmail']
        user.userPasswd = bcrypt.hashpw(data['userPasswd'].encode('utf-8'), bcrypt.gensalt(10))
        db.session.commit()
        return {'message': 'User updated successfully'}, 200

    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200

    @staticmethod
    def check_login(userEmail, userPasswd):
        user = User.query.filter_by(userEmail=userEmail).first()
        if user and bcrypt.checkpw(userPasswd.encode('utf-8'), user.userPasswd.encode('utf-8')):
            return user
        return None
