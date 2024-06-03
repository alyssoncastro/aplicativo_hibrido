from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import requests
from PIL import Image
import traceback



app = Flask(__name__)
CORS(app)  
app.config['UPLOAD_FOLDER'] = 'uploads/'



if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        print("Request method:", request.method)
        print("Request files:", request.files)
        print("Request form:", request.form)
        
        if 'file' not in request.files:
            print("No image part in request")
            return jsonify({'error': 'No image part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            print("No selected file")
            return jsonify({'error': 'No selected file'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"File saved to {filepath}")

        #aplicando o filtro
        img = Image.open(filepath)
        print(f"Image opened: {img.format}, {img.size}, {img.mode}")
        bw_img = img.convert('L')
        processed_filename = 'processed_' + filename
        processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
        bw_img.save(processed_filepath)
        print(f"Processed file saved to {processed_filepath}")

        
        response = requests.post('http://notification_service:5003/notify', json={'message': 'Image processed successfully'})
        print(f"Notification response: {response.status_code}")

        return jsonify({
            'message': 'Image uploaded and processed successfully',
            'original_image': filename,
            'processed_image': processed_filename
        }), 200
    
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()  # Adiciona o stack trace completo ao log
        return jsonify({'error': str(e)}), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
