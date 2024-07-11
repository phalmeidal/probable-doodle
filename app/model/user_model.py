from __init__ import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_passwd = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.userName}>"
