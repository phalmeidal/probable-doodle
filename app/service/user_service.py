import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from model.user_model import User
from __init__ import db

class UserService:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_name(user_name):
        return User.query.filter_by(user_name=user_name).first()

    @staticmethod
    def get_user_by_email(user_email):
        return User.query.filter_by(user_email=user_email).first()

    @staticmethod
    def create_user(data):
        hashed_passwd = bcrypt.hashpw(data['user_passwd'].encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')
        new_user = User(user_name=data['user_name'], user_email=data['user_email'], user_passwd=hashed_passwd)
        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Failed to create user', 'error': str(e)}, 500

    @staticmethod
    def update_user(user, data):
        user.userName = data['user_name']
        user.userEmail = data['user_email']
        user.userPasswd = bcrypt.hashpw(data['user_passwd'].encode('utf-8'), bcrypt.gensalt(10))
        db.session.commit()
        return {'message': 'User updated successfully'}, 200

    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200

    @staticmethod
    def check_login(user_email, user_passwd):
        user = User.query.filter_by(user_email=user_email).first()
        if user and bcrypt.checkpw(user_passwd.encode('utf-8'), user.user_passwd.encode('utf-8')):
            return user
        return None
