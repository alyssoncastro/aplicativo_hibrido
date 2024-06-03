import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, jwt_required, get_jwt_identity
import requests as http_request
from flask_cors import CORS

from database.database import db
from database.models import User, Task

app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["JWT_SECRET_KEY"] = "goku-vs-vegeta"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

with app.app_context():
    db.init_app(app)
    db.create_all()
jwt = JWTManager(app)

# Habilitar CORS
CORS(app, origins='*')
CORS(app, resources={r"/*": {"origins": "*"}})

if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    print("BANCO CRIADO COM UM SUCESSO!")
    sys.exit(0)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/user-login", methods=["GET"])
def user_login():
    return render_template("login.html")

@app.route("/user-register", methods=["GET"])
def user_register():
    return render_template("register.html")

@app.route("/content", methods=["GET"])
@jwt_required()
def content():
    return render_template("content.html")

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")

@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(name=username, password=password).first()
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=user.id)
    response = jsonify({"token": access_token, "user_id": user.id })
    set_access_cookies(response, access_token)
    return response

@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        data = request.json
    else:
        data = request.form
    
    username = data.get("username", None)
    password = data.get("password", None)
    
    if username is None or password is None:
        return render_template("error.html", message="Bad username or password")
    
    token_data = http_request.post(
        "http://localhost:5000/token",
        json={"username": username, "password": password},
        headers={"Content-Type": "application/json"}
    )
    
    if token_data.status_code != 200:
        return render_template("error.html", message="Bad username or password")
    
    response = make_response(render_template("content.html"))
    set_access_cookies(response, token_data.json()['token'])
    return response


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return_users = [user.serialize() for user in users]
    return jsonify(return_users)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize())


@app.route("/users", methods=["POST"])
def create_user():
    if request.is_json:
        data = request.json
    else:
        data = request.form
    user = User(name=data["name"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["PATCH"])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.serialize() for task in tasks])

@app.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task is None:
        return jsonify({"msg": "Task not found"}), 404
    return jsonify(task.serialize())

@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.json
    task = Task(title=data["title"], description=data.get("description", ""), user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.serialize()), 201

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.json
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task is None:
        return jsonify({"msg": "Task not found"}), 404
    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    db.session.commit()
    return jsonify(task.serialize())

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task is None:
        return jsonify({"msg": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Task deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
