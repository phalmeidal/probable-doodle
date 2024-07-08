from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from users import api as users_api

app = Flask(__name__)
CORS(app, resources={r"/users/*": {"origins": "http://localhost:3000"}})
api = Api(app, doc='/docs')

api.add_namespace(users_api, path='/users')

if __name__ == '__main__':
    app.run(debug=True)
    
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
