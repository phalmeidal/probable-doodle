from flask import Flask
from flask_restx import Api
from users import api as users_api

app = Flask(__name__)
api = Api(app, doc='/docs')

api.add_namespace(users_api, path='/users')

if __name__ == '__main__':
    app.run(debug=True)
