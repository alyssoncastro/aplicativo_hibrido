from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@postgres_service:5432/logs_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    user = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/log', methods=['POST'])
def create_log():
    data = request.get_json()
    new_log = Log(action=data['action'], user=data['user'])
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message': 'Log created successfully'}), 201

@app.route('/log', methods=['GET'])
def get_logs():
    logs = Log.query.all()
    return jsonify([{'action': log.action, 'user': log.user, 'timestamp': log.timestamp} for log in logs])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
