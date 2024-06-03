from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    # Imprime a mensagem de notificação recebida no console
    print(f'Notification received: {data["message"]}')
    # Placeholder para lógica de notificação (e.g., envio de e-mail ou push notification)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
