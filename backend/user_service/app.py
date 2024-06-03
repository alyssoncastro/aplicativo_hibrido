from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS  # Adicionar esta linha
from database import db
from models import User
import requests
import os

app = Flask(__name__)
CORS(app)  # Adicionar esta linha para permitir todas as origens
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'


db.init_app(app)

with app.app_context():
    db.create_all()

jwt = JWTManager(app)

@app.route('/')
def home():
    return jsonify({'message': 'rodando'}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(name=data['name'], password=data['password']).first()
    if user:
        access_token = create_access_token(identity={'name': user.name, 'email': user.email})
        # Log the action
        requests.post('http://log_service:5001/log', json={'action': 'login', 'user': user.name})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    print("rodando!")
    app.run(host='0.0.0.0', port=5000, debug=True)
