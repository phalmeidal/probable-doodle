from __init__ import db

class User(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    userEmail = db.Column(db.String(100), unique=True, nullable=False)
    userPasswd = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.userName}>"
